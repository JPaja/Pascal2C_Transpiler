from src.token import Class
from src.nodes import *
from functools import wraps
import pickle


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = tokens.pop(0)
        self.prev = None

    def restorable(call):
        @wraps(call)
        def wrapper(self, *args, **kwargs):
            state = pickle.dumps(self.__dict__)
            result = call(self, *args, **kwargs)
            self.__dict__ = pickle.loads(state)
            return result
        return wrapper

    def eat(self, class_):
        if self.curr.class_ == class_:
            self.prev = self.curr
            self.curr = self.tokens.pop(0)
        else:
            self.die_type(class_.name, self.curr.class_.name)

    def program(self):
        nodes = []
        while self.curr.class_ in [Class.PROCEDURE, Class.FUNCTION]:
            if self.curr.class_ == Class.PROCEDURE:
                self.eat(Class.PROCEDURE)
                id_ = Id(self.curr.lexeme)
                self.eat(Class.ID)
                args = self.args_()
                self.eat(Class.SEMICOLON)
                body = self.body()
                self.eat(Class.SEMICOLON)
                nodes.append(ProcImpl(id_,args,body))
            elif self.curr.class_ == Class.FUNCTION:
                self.eat(Class.FUNCTION)
                id_ = Id(self.curr.lexeme)
                self.eat(Class.ID)
                args = self.args_()
                self.eat(Class.Colon)
                type_ = self.type()
                self.eat(Class.SEMICOLON)
                body = self.body()
                self.eat(Class.SEMICOLON)
                nodes.append(FuncImpl(id_,type_,args,body))
        main = self.body()
        self.eat(Class.DOT)
        return Program(nodes,main)


    def args_(self):
        self.eat(Class.LPAREN)
        declarations = []
        ids =[]
        while(self.curr.class_ != Class.RPAREN):
            id_ = Id(self.curr.lexeme)
            self.eat(Class.ID)
            ids.append(id_)
            if self.curr.class_ == Class.COMMA:
                self.eat(Class.COMMA)
                continue
            self.eat(Class.Colon)
            type_ = self.type()
            declarations.append(Decl(type_, ids.copy(),None))
            ids.clear()
            if self.curr.class_ == Class.COMMA:
                self.eat(Class.COMMA)
        self.eat(Class.RPAREN)
        return declarations

    def array_(self):
        self.eat(Class.LPAREN)
        nodes =[]
        while(self.curr.class_ != Class.RPAREN):
            node = self.factor()
            nodes.append(node)
            if self.curr.class_ == Class.COMMA:
                self.eat(Class.COMMA)
        self.eat(Class.RPAREN)
        return Elems(nodes)

    def body(self):
        vars_ = []
        if(self.curr.class_ == Class.VAR):
            vars_ = self.vars()
        block = self.block()
        return Body(vars_,block)

    def vars(self):
        self.eat(Class.VAR)
        declarations = []
        ids =[]
        while(True):
            id_ = Id(self.curr.lexeme)
            self.eat(Class.ID)
            ids.append(id_)
            if self.curr.class_ == Class.COMMA:
                self.eat(Class.COMMA)
                continue
            self.eat(Class.Colon)
            type_ = self.type()
            value_ = None
            if(self.curr.class_ == Class.EQ):
                self.eat(Class.EQ)
                if(self.curr.class_ == Class.LPAREN):
                    value_ = self.array_()
                else:
                    value_ = self.factor()
            self.eat(Class.SEMICOLON)
            declarations.append(Decl(type_, ids.copy(),value_))
            ids.clear()
            if self.curr.class_ != Class.ID:
                break
        return declarations

    def type(self):
        if self.curr.class_ == Class.TYPE:
            type_ = Type(self.curr.lexeme)
            self.eat(Class.TYPE)
            if self.curr.class_ != Class.LBRACKET:
                return type_
            self.eat(Class.LBRACKET)
            size = self.factor()
            self.eat(Class.RBRACKET)
            return SzArray(type_,size)
        else:
            self.eat(Class.Array)
            self.eat(Class.LBRACKET)
            leftRange = self.factor()
            self.eat(Class.DOTDOT)
            rightRange = self.factor()
            self.eat(Class.RBRACKET)
            self.eat(Class.OF)
            type_ = Type(self.curr.lexeme)
            self.eat(Class.TYPE)
            return RangeArray(type_,leftRange,rightRange)

    def block(self):
        self.eat(Class.BEGIN)
        nodes = self.nodes_untill(Class.END)
        self.eat(Class.END)
        return Block(nodes)

    def nodes_untill(self, token):
        nodes = []
        while self.curr.class_ != token:
            if self.curr.class_ == Class.ID:
                nodes.append(self.id_())
                self.eat(Class.SEMICOLON)
            elif (self.curr.class_ == Class.Exit):
                self.eat(Class.Exit)
                arg = None
                if (self.curr.class_ == Class.LPAREN):
                    self.eat(Class.LPAREN)
                    arg = self.expr()
                    self.eat(Class.RPAREN)
                self.eat(Class.SEMICOLON)
                nodes.append(Exit(arg))
            elif (self.curr.class_ == Class.BREAK):
                nodes.append(Break())
                self.eat(Class.BREAK)
                self.eat(Class.SEMICOLON)
            elif (self.curr.class_ == Class.CONTINUE):
                nodes.append(Continue())
                self.eat(Class.CONTINUE)
                self.eat(Class.SEMICOLON)
            elif (self.curr.class_ == Class.REPEAT):
                nodes.append(Repeat())
                self.eat(Class.REPEAT)
            elif (self.curr.class_ == Class.UNIIL):
                self.eat(Class.UNIIL)
                cond = self.logic()
                nodes.append(Until(cond))
                self.eat(Class.SEMICOLON)
            elif self.curr.class_ == Class.FOR:
                nodes.append(self.for_())
                self.eat(Class.SEMICOLON)
            elif self.curr.class_ == Class.WHILE:
                nodes.append(self.while_())
                self.eat(Class.SEMICOLON)
            elif self.curr.class_ == Class.IF:
                nodes.append(self.if_())
                self.eat(Class.SEMICOLON)
            else:
                self.die_deriv(self.block.__name__)
        return nodes

    def for_(self):
        self.eat(Class.FOR)
        init = self.id_()
        downto = False
        if self.curr.class_ == Class.TO:
            self.eat(Class.TO)
        else:
            downto = True
            self.eat(Class.DOWNTO)
        to = self.expr()
        self.eat(Class.DO)
        block = self.block()
        return For(init, to, block,downto)

    def while_(self):
        self.eat(Class.WHILE)
        cond = self.logic()
        self.eat(Class.DO)
        block = self.block()
        return While(cond, block)
    
    def if_(self):
        statements = []
        else_block = None
        self.eat(Class.IF)
        while True:
            cond = self.logic()
            self.eat(Class.THEN)
            block = self.block()
            statements.append(IfStatement(cond,block))
            if self.curr.class_ != Class.ELSE:
                break
            self.eat(Class.ELSE)
            if self.curr.class_ != Class.IF:
                else_block = self.block()
                break
            self.eat(Class.IF)
        return If(statements, else_block)

    def id_(self):
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        if self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            if id_.value in ['write','writeln','read','readln']:
                args = self.formatargs()
            else:
                args = self.args()
            self.eat(Class.RPAREN)
            return FuncCall(id_, args)
        elif self.curr.class_ == Class.ASSIGN:
            self.eat(Class.ASSIGN)
            expr = self.expr()
            return Assign(id_, expr)
        elif self.curr.class_ == Class.LBRACKET:
            self.eat(Class.LBRACKET)
            index_ = self.expr()
            self.eat(Class.RBRACKET)
            elem = ArrayElem(id_,index_)
            if(self.curr.class_ != Class.ASSIGN):
                return elem
            self.eat(Class.ASSIGN)
            expr = self.expr()
            return Assign(elem, expr)
        else:
            return id_

    def args(self):
        args = []
        while self.curr.class_ != Class.RPAREN:
            if len(args) > 0:
                if self.curr.class_ != Class.COMMA:
                    a = 1
                self.eat(Class.COMMA)
            args.append(self.expr())
        return Args(args)
    
    def formatargs(self):
        args = []
        while self.curr.class_ != Class.RPAREN:
            if len(args) > 0:
                self.eat(Class.COMMA)
            expr = self.expr()
            left = 0
            right = 0
            if self.curr.class_ == Class.Colon:
                self.eat(Class.Colon)
                left =  self.curr.lexeme
                self.eat(Class.INT)
            if self.curr.class_ == Class.Colon:
                self.eat(Class.Colon)
                right =  self.curr.lexeme
                self.eat(Class.INT)
            args.append(FormatArg(expr,left,right))
            
        return Args(args)

    def logic(self):
        first = self.compare()
        while self.curr.class_ in [Class.AND, Class.OR, Class.XOR]:
            if self.curr.class_ == Class.AND:
                op = self.curr.lexeme
                self.eat(Class.AND)
                second = self.compare()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.OR:
                op = self.curr.lexeme
                self.eat(Class.OR)
                second = self.compare()
                first =  BinOp(op, first, second)
            elif self.curr.class_ == Class.XOR:
                op = self.curr.lexeme
                self.eat(Class.XOR)
                second = self.compare()
                first = BinOp(op, first, second)
        return first

    def factor(self):
        if self.curr.class_ == Class.INT:
            no =  self.curr.lexeme
            self.eat(Class.INT)
            return Int(no)
        elif self.curr.class_ == Class.Float:
            no =  self.curr.lexeme
            self.eat(Class.Float)
            return Float(no)
        elif self.curr.class_ == Class.CHAR:
            value = Char(self.curr.lexeme)
            self.eat(Class.CHAR)
            return value
        elif self.curr.class_ == Class.STRING:
            value = String(self.curr.lexeme)
            self.eat(Class.STRING)
            return value
        elif self.curr.class_ == Class.ID:
            return self.id_()
        elif self.curr.class_ in [Class.MINUS, Class.NOT]:
            op = self.curr
            self.eat(self.curr.class_)
            first = None
            if self.curr.class_ == Class.LPAREN:
                self.eat(Class.LPAREN)
                first = self.logic()
                self.eat(Class.RPAREN)
            else:
                first = self.factor()
            return UnOp(op.lexeme, first)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            first = self.logic()
            self.eat(Class.RPAREN)
            return first
        elif self.curr.class_ == Class.SEMICOLON:
            return None
        else:
            self.die_deriv(self.factor.__name__)

    def term(self):
        if self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            first = self.expr()
            self.eat(Class.RPAREN)
        else:
            first = self.factor()
            
        while self.curr.class_ in [Class.STAR, Class.FWDSLASH, Class.DIV,Class.MOD]:
            if self.curr.class_ == Class.STAR:
                op = self.curr.lexeme
                self.eat(Class.STAR)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.FWDSLASH:
                op = self.curr.lexeme
                self.eat(Class.FWDSLASH)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.DIV:
                op = self.curr.lexeme
                self.eat(Class.DIV)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MOD:
                op = self.curr.lexeme
                self.eat(Class.MOD)
                second = self.factor()
                first = BinOp(op, first, second)
        return first

    def expr(self):
        return self.logic()

    def expr2(self):
        first = self.term()
        while self.curr.class_ in [Class.PLUS, Class.MINUS]:
            if self.curr.class_ == Class.PLUS:
                op = self.curr.lexeme
                self.eat(Class.PLUS)
                second = self.term()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MINUS:
                op = self.curr.lexeme
                self.eat(Class.MINUS)
                second = self.term()
                first = BinOp(op, first, second)
        return first

    def compare(self):
        first = self.expr2()
        while self.curr.class_ in [Class.EQ, Class.NEQ, Class.LT, Class.GT, Class.LTE, Class.GTE]:
            if self.curr.class_ == Class.EQ:
                op = self.curr.lexeme
                self.eat(Class.EQ)
                second = self.expr2()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.NEQ:
                op = self.curr.lexeme
                self.eat(Class.NEQ)
                second = self.expr2()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.LT:
                op = self.curr.lexeme
                self.eat(Class.LT)
                second = self.expr2()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.GT:
                op = self.curr.lexeme
                self.eat(Class.GT)
                second = self.expr2()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.LTE:
                op = self.curr.lexeme
                self.eat(Class.LTE)
                second = self.expr2()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.GTE:
                op = self.curr.lexeme
                self.eat(Class.GTE)
                second = self.expr2()
                first = BinOp(op, first, second)
        return first

    def parse(self):
        return self.program()

    def die(self, text):
        raise SystemExit(text)

    def die_deriv(self, fun):
        self.die("Derivation error: {}".format(fun))

    def die_type(self, expected, found):
        self.die("Expected: {}, Found: {}".format(expected, found))
