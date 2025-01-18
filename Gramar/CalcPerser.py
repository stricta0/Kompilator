from sly import Parser, Lexer
from Gramar import CalcLexer
from Gramar import GF1234577
from Errors_custom import PerserError

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', MORETHAN, LESSTHAN, MOREOREQUALTHAN, LESSOREQUALTHAN),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE)
    )

    # Program główny
    @_('PROGRAM IS declarations BEGIN statements END')
    def program(self, p):

        return {'type': 'program', 'declarations': p.declarations, 'statements': p.statements, 'lineno':p.lineno}

    # Reguła do rozpoznawania tablicy z zakresami
    @_('declarations COMMA IDENTIFIER LTABPAREN index_range RTABPAREN')
    def declarations(self, p):
        print("tablica :)")
        return p.declarations + [{"type": "table", "name" : p.IDENTIFIER, "range" : p.index_range, 'lineno':p.lineno}]

    # Deklaracje zmiennych (IDENTIFIER)
    @_('declarations COMMA IDENTIFIER')
    def declarations(self, p):
        return p.declarations + [{"type": "variable", "name" : p.IDENTIFIER, 'lineno':p.lineno}]  # Dodajemy nową zmienną do listy deklaracji


    # Reguła do rozpoznawania zakresu indeksów (start:koniec)
    @_('index COLON index')
    def index_range(self, p):
        return {'start': p.index0, 'end': p.index1}

    # Reguła do rozpoznawania pojedynczego indeksu, który może być ujemny
    @_('MINUS NUMBER')
    def index(self, p):
        return -int(p.NUMBER)

    @_('NUMBER')
    def index(self, p):
        return int(p.NUMBER)

    @_('IDENTIFIER LTABPAREN index_range RTABPAREN')
    def declarations(self, p):
        return [{"type": "table", "name": p.IDENTIFIER, "range": p.index_range, 'lineno':p.lineno}]
    @_('IDENTIFIER')
    def declarations(self, p):
        return [{"type": "variable", "name" : p.IDENTIFIER, 'lineno':p.lineno}]  # Tylko jedna zmienna

    # Instrukcje
    @_('statements statement')
    def statements(self, p):
        return p.statements + [p.statement]


    @_('statement')
    def statements(self, p):
        return [p.statement]



    @_('IDENTIFIER LTABPAREN index_range RTABPAREN ASSIGN expression SEMICOLON')
    def statement(self, p):
        return {'type': 'assignment', 'variable': p.IDENTIFIER, 'value': p.expression, 'lineno':p.lineno}


    # Przypisanie zmiennej
    @_('IDENTIFIER ASSIGN expression SEMICOLON')
    def statement(self, p):

        return {'type': 'assignment', 'variable': p.IDENTIFIER, 'value': p.expression, 'lineno':p.lineno}


    # Instrukcja odczytu
    @_('READ IDENTIFIER SEMICOLON')
    def statement(self, p):

        return {'type': 'read', 'variable': p.IDENTIFIER, 'lineno':p.lineno}

    # Instrukcja wypisania
    @_('WRITE expression SEMICOLON')
    def statement(self, p):

        return {'type': 'write', 'value': p.expression, 'lineno':p.lineno}

    # Reguła dla porównań
    @_('expression MORETHAN expression')
    def check(self, p):
        return {'type': 'comparison', 'operator': '>', 'left': p.expression0, 'right': p.expression1,
                'lineno': p.lineno}

    @_('expression LESSTHAN expression')
    def check(self, p):
        return {'type': 'comparison', 'operator': '<', 'left': p.expression0, 'right': p.expression1,
                'lineno': p.lineno}

    @_('expression MOREOREQUALTHAN expression')
    def check(self, p):
        return {'type': 'comparison', 'operator': '>=', 'left': p.expression0, 'right': p.expression1,
                'lineno': p.lineno}

    @_('expression LESSOREQUALTHAN expression')
    def check(self, p):
        return {'type': 'comparison', 'operator': '<=', 'left': p.expression0, 'right': p.expression1,
                'lineno': p.lineno}

    # Wyrażenie arytmetyczne
    @_('expression PLUS term')
    def expression(self, p):
        return {'type': 'expression', 'left': p.expression, 'operator': '+', 'right': p.term, 'lineno':p.lineno}

    @_('expression MINUS term')
    def expression(self, p):
        return {'type': 'expression', 'left': p.expression, 'operator': '-', 'right': p.term, 'lineno': p.lineno}

    @_('check')
    def expression(self, p):
        return p.check
    @_('term')
    def expression(self, p):
        return p.term

    # Termin (operacje takie jak mnożenie, dzielenie, etc.)
    @_('term TIMES factor')
    def term(self, p):
        return {'type': 'expression', 'left': p.term, 'operator': '*', 'right': p.factor, 'lineno':p.lineno}

    # Termin (operacje takie jak mnożenie, dzielenie, etc.)
    @_('term DIVIDE factor')
    def term(self, p):
        return {'type': 'expression', 'left': p.term, 'operator': '/', 'right': p.factor, 'lineno': p.lineno}

    @_('factor')
    def term(self, p):
        return p.factor

    # Czynnik - może to być liczba lub zmienna
    @_('MINUS NUMBER')
    def factor(self, p):
        return {'type': 'number', 'value': int(p.NUMBER) * -1, 'lineno': p.lineno}

    # Czynnik - może to być liczba lub zmienna
    @_('NUMBER')
    def factor(self, p):
        return {'type': 'number', 'value': int(p.NUMBER), 'lineno':p.lineno}

    @_('IDENTIFIER')
    def factor(self, p):
        return {'type': 'identifier', 'name': p.IDENTIFIER, 'lineno':p.lineno}

    # Obsługa nawiasów
    @_('LPAREN expression RPAREN')
    def factor(self, p):
        return p.expression

    # Obsługa błędów składniowych
    def error(self, p):
        raise PerserError(p.lineno, f"cant proces {p.type} in this context")

