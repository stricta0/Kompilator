from sly import Lexer
from Errors_custom import LexerError

class CalcLexer(Lexer):
    # Tokeny (słowa kluczowe, operatory, symbole)
    tokens = {
        PROGRAM, PROCEDURE, IS, BEGIN, END, READ, WRITE, IF, THEN, ELSE, ENDIF,
        FOR, FROM, TO, DOWNTO, ENDFOR, REPEAT, UNTIL, WHILE, DO, ENDWHILE,
        ASSIGN, IDENTIFIER, NUMBER,
        PLUS, MINUS, TIMES, DIVIDE, MOD, LPAREN, RPAREN, SEMICOLON, COMMA,
        LTABPAREN, RTABPAREN, COLON,
        MOREOREQUALTHAN, LESSOREQUALTHAN, MORETHAN, LESSTHAN, EQUAL, NOTEQUAL
    }

    # Ignorowane znaki (spacje, tabulatory)
    ignore = ' \t'

    # Definicje tokenów (kolejność ma znaczenie)
    PROGRAM = r'PROGRAM'
    PROCEDURE = r'PROCEDURE'
    IS = r'IS'
    BEGIN = r'BEGIN'
    ENDIF = r'ENDIF'
    END = r'END'
    READ = r'READ'
    WRITE = r'WRITE'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    FOR = r'FOR'
    FROM = r'FROM'
    TO = r'TO'
    DOWNTO = r'DOWNTO'
    ENDFOR = r'ENDFOR'
    REPEAT = r'REPEAT'
    UNTIL = r'UNTIL'
    WHILE = r'WHILE'
    DO = r'DO'
    ENDWHILE = r'ENDWHILE'

    ASSIGN = r':='
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MOD = r'%'
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMICOLON = r';'
    COMMA = r','
    LTABPAREN = r'\['
    RTABPAREN = r'\]'
    COLON = r':'
    EQUAL = r'='
    NOTEQUAL = r"!="
    MOREOREQUALTHAN = r'>='
    LESSOREQUALTHAN = r'<='
    MORETHAN = r'>'
    LESSTHAN = r'<'
    # Identyfikatory i liczby
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'

    # Ignorowanie komentarzy (# do końca linii)
    @_(r'\#.*')
    def COMMENT(self, t):
        pass

    # Ignorowanie nowej linii
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    # Obsługa błędów leksykalnych
    def error(self, t):
        raise LexerError(self.lineno, f"Illegal character '{t.value[0]}' file: CalsLexer.py")