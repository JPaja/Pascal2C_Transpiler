import unittest   
import glob
import sys

from src.generator import Generator
from src.parser import Parser
from src.lexer import Lexer
from src.grapher import Grapher
from src.symbolizer import Symbolizer

class Tests(unittest.TestCase):

	def test_lexer(self):
		for path in glob.glob("test/grader/*/src.pas"):
			with open(path, 'r') as source:
				try:
					text = source.read()
					lexer = Lexer(text)
					lexer.lex()
				except:
					ex = sys.exc_info()[0]
					self.fail("Failed to lex " + path + "\n"+ ex)
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
				except:
					ex = sys.exc_info()[0]
					self.fail("Failed to parse " + path + "\n"+ ex)
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

	def test_symbolizer(self):
		for path in glob.glob("test/grader/*/src.pas"):
			with open(path, 'r') as source:
				print(f"testing {path}")
				text = source.read()
				lexer = Lexer(text)
				tokens = lexer.lex()
				parser = Parser(tokens)
				ast = parser.parse()
				symbolizer = Symbolizer(ast)
				symbolizer.symbolize()

		self.assertTrue(True)

	def test_grapher(self):
		for path in glob.glob("test/grader/08/src.pas"):
			with open(path, 'r') as source:
				print(f"testing {path}")
				text = source.read()
				lexer = Lexer(text)
				tokens = lexer.lex()
				parser = Parser(tokens)
				ast = parser.parse()
				grapher = Generator(ast)
				grapher.generate()
				grapher.write('tmp/sample.c')

		self.assertTrue(True)

#Tests().test_grapher()