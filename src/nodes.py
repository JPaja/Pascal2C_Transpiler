class Node():
    pass


class Program(Node):
    def __init__(self, funcs,main):
        self.funcs = funcs
        self.main = main


class Body(Node):
    def __init__(self, variables,block):
        self.variables = variables
        self.body = block

class Decl(Node):
    def __init__(self, type_, ids_, value):
        self.type_ = type_
        self.ids_ = ids_
        self.value = value


class SzArray(Node):
    def __init__(self, type_, size):
        self.type_ = type_
        self.size = size

class RangeArray(Node):
    def __init__(self, type_, leftRange, rightRange):
        self.type_ = type_
        self.leftRange = leftRange
        self.rightRange = rightRange

class ArrayElem(Node):
    def __init__(self, id_, index):
        self.id_ = id_
        self.index = index


class Assign(Node):
    def __init__(self, id_, expr):
        self.id_ = id_
        self.expr = expr


class If(Node):
    def __init__(self, cond, true, false):
        self.cond = cond
        self.true = true
        self.false = false


class While(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class For(Node):
    def __init__(self, init, to, block):
        self.init = init
        self.to = to
        self.block = block


class FuncImpl(Node):
    def __init__(self, type_, id_, params, body):
        self.type_ = type_
        self.id_ = id_
        self.params = params
        self.body = body

class ProcImpl(Node):
    def __init__(self, id_, params, body):
        self.id_ = id_
        self.params = params
        self.body = body


class FuncCall(Node):
    def __init__(self, id_, args):
        self.id_ = id_
        self.args = args


class Block(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Args(Node):
    def __init__(self, args):
        self.args = args


class Exit(Node):
    def __init__(self):
        return

class Break(Node):
    def __init__(self):
        return

class Continue(Node):
    def __init__(self):
        return


class Until(Node):
    def __init__(self,block,cond):
        self.block = block
        self.cond = cond

class Type(Node):
    def __init__(self, value):
        self.value = value


class Int(Node):
    def __init__(self, value):
        self.value = value


class Char(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Id(Node):
    def __init__(self, value):
        self.value = value


class BinOp(Node):
    def __init__(self, symbol, first, second):
        self.symbol = symbol
        self.first = first
        self.second = second


class UnOp(Node):
    def __init__(self, symbol, first):
        self.symbol = symbol
        self.first = first
