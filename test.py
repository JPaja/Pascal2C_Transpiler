import unittest   
import glob
from src.parser import Parser
from src.lexer import Lexer
from src.grapher import Grapher

class Tests(unittest.TestCase):


	def test_lexer(self):
		for path in glob.glob("test/grader/*/src.pas"):
			with open(path, 'r') as source:
				try:
					text = source.read()
					lexer = Lexer(text)
					lexer.lex()
				except Exception as ex:
					self.fail("Failed to lex "+ path + "\n"+ ex)
		self.assertTrue(True)
	
	def test_parser(self):
		for path in glob.glob("test/grader/*/src.pas"):
			with open(path, 'r') as source:
				try:
					text = source.read()
					lexer = Lexer(text)
					tokens = lexer.lex()
					parser = Parser(tokens)
					parser.parse()
				except Exception as ex:
					self.fail("Failed to parse "+ path + "\n"+ ex)
		self.assertTrue(True)
	
	def test_grapher(self):
		for path in glob.glob("test/grader/*/src.pas"):
			with open(path, 'r') as source:
				print(f"testing {path}")
				text = source.read()
				lexer = Lexer(text)
				tokens = lexer.lex()
				parser = Parser(tokens)
				ast = parser.parse()
				grapher = Grapher(ast)
				dot = grapher.graph()
				grapher.save()
		self.assertTrue(True)               

#Tests().test_grapher()