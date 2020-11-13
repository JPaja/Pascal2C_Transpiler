import unittest   
import glob
from src.parser import Parser
from src.lexer import Lexer

class Tests(unittest.TestCase):
	def test_lexer(self):
		for path in glob.glob("test/pas/*11.pas"):
			with open(path, 'r') as source:
				text = source.read()
				lexer = Lexer(text)
				lexer.lex()
		self.assertTrue(True)
	
	def test_parser(self):
		for path in glob.glob("test/pas/*.pas"):
			with open(path, 'r') as source:
				print(f"testing {path}")
				text = source.read()
				lexer = Lexer(text)
				tokens = lexer.lex()
				parser = Parser(tokens)
				parser.parse()
		self.assertTrue(True)

