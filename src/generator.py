from src.nodes import Type, SzArray, RangeArray, Assign
from src.visitor import Visitor
import re
import os


class Generator(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.py = ""
        self.level = 0

    def append(self, text):
        self.py += str(text)

    def newline(self):
        self.append('\n')

    def indent(self):
        for i in range(self.level):
            self.append('\t')

    def generate(self):
        self.visit(None, self.ast)
        self.py = re.sub('\n\s*\n', '\n', self.py)
        return self.py

    def write(self, path):
        with open(path, 'w') as source:
            source.write(self.py)
        return path
    def die(self, text):
        raise SystemExit(text)

    def visit_Program(self, parent, node):
        for n in node.funcs:
            self.visit(node, n)
        self.append("int main() ")
        self.append("{")
        self.visit(node, node.main)
        self.append("return 0;")
        self.newline()
        self.append("}")

    def visit_FuncImpl(self, parent, node):
        self.visit(node.type_)
        self.append(' ')
        self.visit(node.id_)
        self.append('(')
        i = 0
        for n in node.params:
            for p in n.ids_:
                if i != 0:
                    self.append(',')
                self.visit(node, n.type_)
                self.append(' ')
                self.visit(node, p)
        self.append(')')
        self.newline()
        self.append("{")
        self.level += 1
        self.visit(node, node.body)
        self.level -= 1
        self.append("}")

    def visit_ProcImpl(self, parent, node):
        self.append('void ')
        self.visit(node,node.id_)
        self.append('(')
        i = 0
        for n in node.params:
            for p in n.ids_:
                if i != 0:
                    self.append(',')
                i += 1
                self.visit(node, n.type_)
                self.append(' ')
                self.visit(node, p)
        self.append(')')
        self.newline()
        self.append("{")
        self.level += 1
        self.visit(node, node.body)
        self.level -= 1
        self.append("}")


    def visit_Body(self, parent, node):
        self.newline()
        for n in node.variables:
            self.visit(node, n)
        self.visit(node, node.block)

    def getType(self, type_):
        if type_ is Type:
            return type_
        if type is SzArray:
            return type_.type_
        if type is RangeArray:
            return type_.type_
        return type_

    # def arraySize(self, type_):
    #     if type_ is SzArray:
    #         return type_.size
    #     if type_ is RangeArray:
    #         left = type_.leftRange
    #         right = type_.rightRange
    #         if left is not 1:
    #             self.die("Start index is not 1") #return -1 #TODO: Support array index subtraction
    #         return right
    #     return  None

    def visit_Decl(self, parent, node):
        self.indent()
        self.visit(node, self.getType(node.type_))
        self.append(' ')
        i = 0
        for n in node.ids_:
            if i != 0:
                self.append(',')
            i+=1
            self.visit(node, n)
            if node.type_ is SzArray:
                self.append('[')
                self.visit(node.type_.size)
                self.append(']')
            elif node.type_ is RangeArray:
                self.append('[')
                self.visit(node.type_.rightRange)
                self.append(']')
            if node.value is not None:
                self.append('=')
                self.visit(node, node.value)
        self.append(';')
        self.newline()

    def visit_Type(self, parent, node):
        if node.value == 'integer':
            self.append('int')
        elif node.value == 'boolean':
            self.append('bool')
        else:
            self.append(node.value)

    def visit_SzArray(self, parent, node):
        self.append(node.type_)
        self.append("[")
        self.visit(node, node.size)
        self.append("]")
        # self.add_node(parent, node)
        # self.visit(node, node.type_)
        # self.visit(node, node.size)

    def visit_RangeArray(self, parent, node):
        self.append(node.type_)
        self.append("[")
        self.visit(node, node.rightRange)
        self.append("]")
        # self.add_node(parent, node)
        # self.visit(node, node.type_)
        # self.visit(node, node.leftRange)
        # self.visit(node, node.rightRange)

    def visit_ArrayElem(self, parent, node):
        self.visit(node, node.id_)
        self.append('[')
        self.visit(node.index)
        self.append(']')

    def visit_Assign(self, parent, node):
        self.visit(node, node.id_)
        self.append('=')
        self.visit(node, node.expr)

    def visit_If(self, parent, node):
        i = 0
        for statement in node.statements:
            self.indent()
            if i != 0:
                self.append('else')
            i+=1
            self.append('if(')
            self.visit(node, statement.cond)
            self.append(')')
            self.newline()
            self.indent()
            self.append('{')
            self.level+=1
            self.visit(node, statement.block)
            self.level -= 1
            self.indent()
            self.append('}')

        if (node.else_block is not None):
            self.indent()
            self.append('else')
            self.newline()
            self.indent()
            self.append('{')
            self.level += 1
            self.visit(node, node.else_block)
            self.level -= 1
            self.indent()
            self.append('}')

    def visit_IfStatement(self, parent, node):
        pass
        # self.add_node(parent, node)
        # self.visit(node, node.cond)
        # self.visit(node, node.block)

    def visit_While(self, parent, node):
        self.indent()
        self.append('while(')
        self.visit(node, node.cond)
        self.append(')')
        self.newline()
        self.indent()
        self.append('{')
        self.level += 1
        self.visit(node, node.block)
        self.level -= 1
        self.indent()
        self.append('}')


    def visit_For(self, parent, node):
        self.indent()
        self.append('for(')
        self.visit(node, node.init)
        self.append(';')
        if node.init is not Assign:
            self.die("For init is not assign")
        self.visit(node.init.id_)
        if(node.downto):
            self.append('>=')
        else:
            self.append('<=')
        self.visit(node, node.to)
        self.append(';')
        self.visit(node.init.id_)
        if (node.downto):
            self.append('++')
        else:
            self.append('--')
        self.append('for)')
        self.newline()
        self.indent()
        self.append('{')
        self.level += 1
        self.visit(node, node.block)
        self.level -= 1
        self.indent()
        self.append('}')


    def visit_FuncCall(self, parent, node):
        id_ = node.id_.value
        if(id_ in ['readln','read','write','writeln']):
            if id_ in ['readln','read']:
                self.append('scanf')
                self.visit_FormatedArgs(node, node.args, True)
            elif id_ in ['write','writeln']:
                self.append('printf')
                self.visit_FormatedArgs(node, node.args, False)
        elif id_ in ['chr', 'ord']:
            self.visit(node, node.args.args[0])
        else:
            self.visit(node,node.id_)
            self.visit(node,node.args)

    def visit_Block(self, parent, node):
        self.newline()
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            self.append(';')
            self.newline()


    def visit_Params(self, parent, node):
        self.append('(')
        i = 0
        for n in node.params:
            if i != 0:
                self.append(',')
            i+=1
            self.visit(node, n)
        self.append(')')

    def visit_Args(self, parent, node):
        self.append('(')
        i = 0
        for n in node.args:
            if i != 0:
                self.append(',')
            i+=1
            self.visit(node, n)
        self.append(')')

    def visit_FormatedArgs(self, parent, node, write):
        self.append('(\"')
        for n in node.args:
            self.append(self.scanType(n))
        self.append('\"')
        for n in node.args:
            self.append(', ')
            if write:
                self.append('&')
            self.visit(node, n)
        self.append(')')

    def scanType(self, arg):
        return '%d'

    def visit_FormatArg(self, parent, node):
        #TODO Detect printf and scanf parameters
        self.visit(node,node.arg)
        # i = 0
        # for n in node.args:
        #     if i != 0:
        #         self.append(',')
        #     i += 1
        #     self.visit(node, n)
        # self.append(')')

    def visit_Elems(self, parent, node):
        self.append('{')
        i = 0
        for n in node.values:
            if i != 0:
                self.append(',')
            i += 1
            self.visit(node, n)
        self.append('}')

    def visit_Exit(self, parent, node):
        self.append('return 0')

    def visit_Break(self, parent, node):
        self.append('break')

    def visit_Continue(self, parent, node):
        self.append('continue')

    def visit_Until(self, parent, node):
        self.indent()

        self.append(' o {')
        self.level += 1
        self.visit(node, node.block)
        self.level -= 1
        self.indent()
        self.append('}')
        self.append('while(')
        self.visit(node, node.cond)
        self.append(')')


    def visit_Int(self, parent, node):
        name = node.value
        self.append(name)

    def visit_Float(self, parent, node):
        name = node.value
        self.append(name)

    def visit_Char(self, parent, node):
        name = node.value
        self.append('\'')
        self.append(name)
        self.append('\'')

    def visit_String(self, parent, node):
        name = node.value
        self.append('"')
        self.append(name)
        self.append('"')

    def visit_Id(self, parent, node):
        name = node.value
        self.append(name)

    def visit_BinOp(self, parent, node):
        name = node.symbol
        self.append('(')
        self.visit(node, node.first)
        self.append(' ')
        if(name == 'div'):
            self.append('/')
        elif(name == 'mod'):
            self.append('%')
        elif (name == 'and'):
            self.append('&&')
        elif (name == 'or'):
            self.append('||')
        elif (name == 'xor'):
            self.append('^')
        else:
            self.append(name)
        self.append(' ')
        self.visit(node, node.second)
        self.append(')')

    def visit_UnOp(self, parent, node):
        name = node.symbol
        self.append(name)
        self.visit(node, node.first)