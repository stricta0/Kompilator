from sly import Lexer

class CalcLexer(Lexer):
    tokens = { NEGATIVE, NUMBER, PLUS, MINUS, TIMES, DIVIDE, POWER, LPAREN, RPAREN }
    ignore = ' \t'

    # Definicje tokenów
    NEGATIVE = r'-\d+'
    NUMBER = r'\d+'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r':'
    POWER = r'\^'
    LPAREN = r'\('
    RPAREN = r'\)'

    # Ignorowanie nowej linii
    @_(r'\n+')
    def newline(self, t):
        pass
