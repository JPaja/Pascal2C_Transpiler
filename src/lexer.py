from src.token import Class, Token

class Lexer:
	def __init__(self, text):
		self.text = text
		self.len = len(text)
		self.pos = -1

	def read_space(self):
		while self.pos + 1 < self.len and self.text[self.pos + 1].isspace():
			self.next_char()

	def read_int(self):
		lexeme = self.text[self.pos]
		while self.pos + 1 < self.len and self.text[self.pos + 1].isdigit():
			lexeme += self.next_char()
		return int(lexeme)

	def read_char(self):
		lexeme = ''
		while self.pos + 1 < self.len and self.text[self.pos + 1] != '\'':
			lexeme += self.next_char()
		self.pos += 1
		return lexeme

	def read_string(self):
		lexeme = ''
		while self.pos + 1 < self.len and self.text[self.pos + 1] != '"':
			lexeme += self.next_char()
		self.pos += 1
		return lexeme

	def read_keyword(self):
		lexeme = self.text[self.pos]
		while self.pos + 1 < self.len and self.text[self.pos + 1].isalnum():
			lexeme += self.next_char()
		if lexeme == 'div':
			return Token(Class.DIV,lexeme)
		elif lexeme == 'mod':
			return Token(Class.MOD,lexeme)
		elif lexeme == 'not':
			return Token(Class.NOT,lexeme)
		elif lexeme == 'or':
			return Token(Class.OR,lexeme)
		elif lexeme == 'xor':
			return Token(Class.OR,lexeme)
		elif lexeme == 'and':
			return Token(Class.AND,lexeme)
		elif lexeme == 'begin':
			return Token(Class.BEGIN,lexeme)
		elif lexeme == 'end':
			return Token(Class.END,lexeme)
		elif lexeme == 'if':
			return Token(Class.IF,lexeme)
		elif lexeme == 'else':
			return Token(Class.ELSE,lexeme)
		elif lexeme == 'then':
			return Token(Class.THEN,lexeme)
		elif lexeme == 'for':
			return Token(Class.FOR,lexeme)
		elif lexeme == 'to':
			return Token(Class.TO,lexeme)
		elif lexeme == 'do':
			return Token(Class.DO,lexeme)
		elif lexeme == 'while':
			return Token(Class.WHILE,lexeme)
		elif lexeme == 'break':
			return Token(Class.BREAK,lexeme)
		elif lexeme == 'continue':
			return Token(Class.CONTINUE,lexeme)
		elif lexeme == 'repeat':
			return Token(Class.REPEAT,lexeme)
		elif lexeme == 'until':
			return Token(Class.UNIIL,lexeme)
		elif lexeme == 'var':
			return Token(Class.VAR,lexeme)
		elif lexeme == 'of':
			return Token(Class.OF,lexeme)
		elif lexeme == 'procedure':
			return Token(Class.PROCEDURE,lexeme)
		elif lexeme == 'function':
			return Token(Class.FUNCTION,lexeme)
		elif lexeme == 'integer' or lexeme == 'char' or lexeme == 'string' or lexeme == 'real':
			return Token(Class.TYPE, lexeme)
		elif lexeme == 'array':
			return Token(Class.Array, lexeme)
		elif lexeme == 'exit':
			return Token(Class.Exit, lexeme)
		return Token(Class.ID, lexeme)

	def next_char(self):
		self.pos += 1
		if self.pos >= self.len:
			return None
		return self.text[self.pos]

	def next_token(self):
		self.read_space()
		curr = self.next_char()
		if curr is None:
			return Token(Class.EOF, curr)
		if curr.isalpha():
			return self.read_keyword()
		elif curr.isdigit():
			return Token(Class.INT, self.read_int())
		elif curr == '\'':
			return Token(Class.CHAR, self.read_char())
		elif curr == '"':
			return Token(Class.STRING, self.read_string())
		elif curr == ':':
			curr = self.next_char()
			if curr == '=':
					return Token(Class.ASSIGN, ':=')
			self.pos -= 1
			return Token(Class.Colon, ':')
		elif curr == '+':
			return Token(Class.PLUS, curr)
		elif curr == '-':
			return Token(Class.MINUS, curr)
		elif curr == '*':
			return Token(Class.STAR, curr)
		elif curr == '/':
			return Token(Class.FWDSLASH, curr)
		elif curr == '=':
			return Token(Class.EQ, curr)
		elif curr == '<':
			curr = self.next_char()
			if curr == '>':
					return Token(Class.NEQ, '<>')
			elif curr == '=':
					return Token(Class.LTE, '<=')
			self.pos -= 1
			return Token(Class.LT, '<')
		elif curr == '>':
			curr = self.next_char()
			if curr == '=':
					return Token(Class.GTE, '>=')
			self.pos -= 1
			return Token(Class.GT, '>')
		elif curr == '(':
			return Token(Class.LPAREN, curr)
		elif curr == ')':
			return Token(Class.RPAREN, curr)
		elif curr == '[':
			return Token(Class.LBRACKET, curr)
		elif curr == ']':
			return Token(Class.RBRACKET, curr)
		elif curr == ';':
			return Token(Class.SEMICOLON, curr)
		elif curr == ',':
			return Token(Class.COMMA, curr)
		elif curr == '.':
			curr = self.next_char();
			if curr == '.':
				return Token(Class.DOTDOT, '..')
			self.pos -= 1
			return Token(Class.DOT, '.')
		self.die(curr)

	def lex(self):
		tokens = []
		while True:
			curr = self.next_token()
			tokens.append(curr)
			if curr.class_ == Class.EOF:
					break
		return tokens

	def die(self, char):
		raise SystemExit("Unexpected character: {}".format(char))
