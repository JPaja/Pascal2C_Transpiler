from numbers import Real

from src.nodes import Type, SzArray, RangeArray, Assign, Id, FuncImpl, Int, Bool, String, Char, FormatArg, ArrayElem, \
    FuncCall, BinOp, UnOp
from src.visitor import Visitor
import re
import os


class Generator(Visitor):
    def __init__(self, ast, symbolizer):
        self.ast = ast
        self.py = ""
        self.symbolizer = symbolizer
        self.level = 0
        self.varMap = {}

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
        res = '#include <stdio.h>\n' \
              '#include <string.h>\n\n'
        res += self.py
        with open(path, 'w') as source:
            source.write(res)
        return path
    def die(self, text):
        raise SystemExit(text)

    def visit_Program(self, parent, node):

        for n in node.funcs:
            self.visit_FuncSig(node, n)
        self.newline()
        for n in node.funcs:
            self.visit(node, n)
        self.append("int main() ")
        self.append("{")
        self.visit(node, node.main)
        self.append("return 0;")
        self.newline()
        self.append("}")

    def visit_FuncSig(self, parent, node):
        if isinstance(node, FuncImpl):
            self.visit(node, node.type_)
        else:
            self.append('void')
        self.append(' ')
        self.visit(node, node.id_)
        self.append('(')
        i = 0
        for n in node.params:
            for p in n.ids_:
                if i != 0:
                    self.append(',')
                i += 1
                self.visit(node, n.type_)
        self.append(');')
        self.newline()

    def visit_FuncImpl(self, parent, node):
        for symb in node.symbols:
            self.varMap[symb.id_] = symb.type_
        self.visit(node, node.type_)
        self.append(' ')
        self.visit(node, node.id_)
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

    def visit_ProcImpl(self, parent, node):
        for symb in node.symbols:
            self.varMap[symb.id_] = symb.type_
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
        for symb in node.symbols:
            self.varMap[symb.id_] = symb.type_

        self.newline()
        for n in node.variables:
            self.visit(node, n)
        self.visit(node, node.block)

    def getType(self, type_):
        if type_ is Type:
            return type_
        if isinstance(type_,SzArray):
            return type_.type_
        if isinstance(type_,RangeArray):
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
        type_ = self.getType(node.type_)
        if type_.value == 'string':
            self.append('char')
        else:
            self.visit(node, type_)
        self.append(' ')
        i = 0
        for n in node.ids_:
            if i != 0:
                self.append(',')
            i+=1
            self.visit(node, n)
            if isinstance(node.type_, SzArray):
                self.append('[')
                self.visit(node.type_, node.type_.size)
                self.append(']')
            elif isinstance(node.type_ , RangeArray):
                self.append('[')
                self.visit(node.type_, node.type_.rightRange)
                #self.append(node.type_.rightRange)
                self.append(']')
            elif type_.value == 'string':
                self.append('[100] = {0}')
            if node.value is not None:
                self.append('=')
                self.visit(node, node.value)
        self.append(';')
        self.newline()

    def visit_Type(self, parent, node):
        if node.value == 'integer':
            self.append('int')
        elif node.value == 'boolean':
            self.append('int')
        elif node.value == 'real':
            self.append('float')
        elif node.value == 'string':
            self.append('char*')
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
        self.visit(node,node.index)
        self.append(']')

    def visit_Assign(self, parent, node):
        self.visit(node, node.id_)
        self.append('=')
        self.visit(node, node.expr)

    def visit_If(self, parent, node):
        i = 0
        for statement in node.statements:
            if i != 0:
                self.indent()
                self.append('else ')
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
        self.append('for(')
        self.visit(node, node.init)
        self.append(';')
        if isinstance(node.init,Assign) is False:
            self.die("For init is not assign")
        self.visit(node.init,node.init.id_)
        if(node.downto):
            self.append('>=')
        else:
            self.append('<=')
        self.visit(node, node.to)
        self.append(';')
        self.visit(node.init,node.init.id_)
        if (node.downto):
            self.append('--')
        else:
            self.append('++')
        self.append(')')
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
                self.visit_FormatedArgs(node.id_, node.args, True)
            elif id_ in ['write','writeln']:
                self.append('printf')
                self.visit_FormatedArgs(node.id_, node.args, False)
        elif id_ in ['chr', 'ord'] and len(node.args.args) == 1:
            self.visit(node, node.args.args[0])
        elif id_ == 'inc' and len(node.args.args) == 1 and isinstance(node.args.args[0], Id):
            self.visit(node, node.args.args[0])
            self.append(" = ")
            self.visit(node, node.args.args[0])
            self.append(" + 1")
        elif id_ == 'length' and len(node.args.args) == 1:
            self.append('strlen')
            self.visit(node,node.args)
        elif id_ == 'insert' and len(node.args.args) == 3:
            self.visit(node, node.args.args[1])
            self.append("[")
            self.visit(node, node.args.args[2])
            self.append("] = ")
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
            left = None
            right = None
            if isinstance(n, FormatArg):
                left = n.left
                right = n.right
            self.append(self.scanType(node, n.arg, left, right))
        if(parent.value == 'writeln'):
            self.append('\\n')
        self.append('\"')
        for n in node.args:
            self.append(', ')
            if write: #TODO check if alredy pointer (string)
                self.append('&')
            self.visit(node, n)
        self.append(')')

    def scanType(self,parent, arg, left, right):
        if isinstance(arg, Id):
            if id in self.varMap:
                return self.scanType(arg, self.varMap[arg], left, right)
            return None
        if isinstance(arg, ArrayElem):
            return self.scanType(arg, arg.id_, left, right)
        if isinstance(arg, FuncCall):
            return self.scanType(arg, arg.id_, left, right)
        if isinstance(arg, BinOp):
            return self.scanType(arg, arg.first, left, right)
        if isinstance(arg, UnOp):
            return self.scanType(arg, arg.first, left, right)
        prefix = '%'
        if left is not None and isinstance(left, Int):
            prefix += str(left.value) + '.'
        if right is not None and isinstance(right, Int):
            prefix += str(right.value)
        if isinstance(arg, Int) or isinstance(arg, Bool):
            return prefix+'d'
        if isinstance(arg, Real):
            return prefix+'f'
        if isinstance(arg, Char) and len(arg.value) == 1:
            return prefix+'c'
        if isinstance(arg, String) or isinstance(arg, Char):
            return prefix+'s'
        if isinstance(arg, Type):
            name = arg.value
            if name == 'integer':
                return prefix+'d'
            elif name == 'real':
                return prefix+'f'
            elif name == 'string':
                return prefix+'s'
        return None

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
        self.append('return ')
        if node.arg is not None:
            self.visit(node, node.arg)
        # else:
        #    self.append('0')

    def visit_Break(self, parent, node):
        self.append('break')

    def visit_Continue(self, parent, node):
        self.append('continue')

    def visit_Until(self, parent, node):
        self.indent()

        self.append('do {')
        self.level += 1
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            self.append(';')
            self.newline()
        self.level -= 1
        self.indent()
        self.append('}')
        self.append('while(')
        self.visit(node, node.cond)
        self.append(')')


    def visit_Int(self, parent, node):
        name = node.value
        self.append(name)

    def visit_Bool(self, parent, node):
        name = node.value
        if(name is True):
            self.append('0')
        else:
            self.append('1')

    def visit_Float(self, parent, node):
        name = node.value
        self.append(name)

    def visit_Char(self, parent, node):
        name = node.value
        if(len(name) <= 1):
            self.append('\'')
            self.append(name)
            self.append('\'')
        else:
            self.append('\"')
            self.append(name)
            self.append('\"')

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
        elif (name == '='):
            self.append('==')
        elif (name == '<>'):
            self.append('!=')
        else:
            self.append(name)
        self.append(' ')
        self.visit(node, node.second)
        self.append(')')

    def visit_UnOp(self, parent, node):
        name = node.symbol
        self.append(name)
        self.visit(node, node.first)