from enum import Enum, auto


class Class(Enum):
    ID = auto()
    EOF = auto()
    Exit = auto()

    Array = auto()
    TYPE = auto()
    INT = auto()
    CHAR = auto()
    STRING = auto()

    ASSIGN = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    FWDSLASH = auto()
    DIV = auto()
    MOD = auto()

    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()

    OR = auto()
    AND = auto()
    NOT = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()

    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    Colon = auto()
    DOTDOT = auto()

    BEGIN = auto()
    END  = auto()

    IF = auto()
    ELSE = auto()
    THEN = auto()

    FOR = auto()
    TO = auto()
    WHILE = auto()
    DO = auto()

    VAR = auto()
    OF = auto()
    PROCEDURE = auto()
    FUNCTION = auto()

class Token:
    def __init__(self, class_, lexeme):
        self.class_ = class_
        self.lexeme = lexeme

    def __str__(self):
        return "<{} {}>".format(self.class_, self.lexeme)
