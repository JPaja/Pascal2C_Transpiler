from src.nodes import Type, SzArray, RangeArray
from src.symbols import Symbols
from src.visitor import Visitor


class Symbolizer(Visitor):
    def __init__(self, ast):
        self.ast = ast

    def symbolize(self):
        self.visit(None, self.ast)

    def visit_Program(self, parent, node):
        node.symbols = Symbols()
        for n in node.funcs:
            self.visit(node, n)
        self.visit(node, node.main)

    def visit_Body(self, parent, node):
        node.symbols = Symbols()
        for v in node.variables:
            self.visit(node, v)
        pass

    def getType(self, type_):
        if type_ is Type:
            return type_
        if type is SzArray:
            return type_.type_
        if type is RangeArray:
            return type_.type_
        return type_

    def visit_Decl(self, parent, node):
        for id_ in node.ids_:
            parent.symbols.put(id_, node.type_, id(parent))

    def visit_FuncImpl(self, parent, node):
        node.symbols = Symbols()
        parent.symbols.put(node.id_, node.type_, id(parent))
        self.visit(node, node.body)

    def visit_ProcImpl(self, parent, node):
        # TODO: Check what to do for type
        node.symbols = Symbols()
        parent.symbols.put(node.id_, Type('void'), id(parent))
        self.visit(node, node.body)

    def visit_SzArray(self, parent, node):
        pass

    def visit_RangeArray(self, parent, node):
        pass

    def visit_ArrayElem(self, parent, node):
        pass

    def visit_Assign(self, parent, node):
        pass

    def visit_If(self, parent, node):
        pass

    def visit_IfStatement(self, parent, node):
        pass

    def visit_While(self, parent, node):
        pass

    def visit_For(self, parent, node):
        pass

    def visit_FuncCall(self, parent, node):
        pass

    def visit_Block(self, parent, node):
        pass

    def visit_Params(self, parent, node):
        pass

    def visit_Args(self, parent, node):
        pass

    def visit_FormatArg(self, parent, node):
        pass

    def visit_Elems(self, parent, node):
        pass

    def visit_Exit(self, parent, node):
        pass

    def visit_Break(self, parent, node):
        pass

    def visit_Continue(self, parent, node):
        pass

    def visit_Repeat(self, parent, node):
        pass

    def visit_Until(self, parent, node):
        pass

    def visit_Type(self, parent, node):
        pass

    def visit_Int(self, parent, node):
        pass

    def visit_Bool(self, parent, node):
        pass

    def visit_Float(self, parent, node):
        pass

    def visit_Char(self, parent, node):
        pass

    def visit_String(self, parent, node):
        pass

    def visit_Id(self, parent, node):
        pass

    def visit_BinOp(self, parent, node):
        pass

    def visit_UnOp(self, parent, node):
        pass
