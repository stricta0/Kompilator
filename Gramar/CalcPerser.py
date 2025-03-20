from sly import Parser, Lexer
from Gramar import CalcLexer
from Errors_custom import PerserError

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', MORETHAN, LESSTHAN, MOREOREQUALTHAN, LESSOREQUALTHAN, EQUAL, NOTEQUAL),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE, MOD)
    )
    @_('procedures program')
    def program_all(self, p):
        return {'procedures': p.procedures, 'program' : p.program}

    @_('program')
    def program_all(self, p):
        return {'procedures': None, 'program' : p.program}

    @_('procedures PROCEDURE proc_head IS declarations BEGIN statements END')
    def procedures(self, p):
        return p.procedures + [{"type" : "procedure", "declarations" : p.declarations, "body": p.statements, "head" : p.proc_head, 'lineno':p.lineno}]

    @_('procedures PROCEDURE proc_head IS BEGIN statements END')
    def procedures(self, p):
        return p.procedures + [{"type" : "procedure", "declarations" : [], "body": p.statements, "head" : p.proc_head, 'lineno':p.lineno}]

    @_('PROCEDURE proc_head IS declarations BEGIN statements END')
    def procedures(self, p):
        return [{"type" : "procedure", "declarations" : p.declarations, "body": p.statements, "head" : p.proc_head, 'lineno':p.lineno}]

    @_('PROCEDURE proc_head IS BEGIN statements END')
    def procedures(self, p):
        return [{"type" : "procedure", "declarations" : [], "body": p.statements, "head" : p.proc_head, 'lineno':p.lineno}]


    @_('IDENTIFIER LPAREN args_decl RPAREN')
    def proc_head(self, p):
        return {"type": "proc_head", "name" : p.IDENTIFIER, "args": p.args_decl, 'lineno':p.lineno}

    @_('IDENTIFIER LPAREN RPAREN')
    def proc_head(self, p):
        return {"type": "proc_head", "name": p.IDENTIFIER, "args": [], 'lineno':p.lineno}

    @_('args_decl COMMA IDENTIFIER')
    def args_decl(self, p):
        return p.args_decl + [{"type": "variable", "name" : p.IDENTIFIER, 'lineno':p.lineno}]

    @_('args_decl COMMA T IDENTIFIER')
    def args_decl(self, p):
        return p.args_decl + [{"type": "table", "name": p.IDENTIFIER, 'lineno':p.lineno}]

    @_('IDENTIFIER')
    def args_decl(self, p):
        return [{"type": "variable", "name" : p.IDENTIFIER, 'lineno':p.lineno}]

    @_('T IDENTIFIER')
    def args_decl(self, p):
        return [{"type": "table", "name": p.IDENTIFIER, 'lineno':p.lineno}]
    # Program główny
    @_('PROGRAM IS declarations BEGIN statements END')
    def program(self, p):

        return {'type': 'program', 'declarations': p.declarations, 'statements': p.statements, 'lineno':p.lineno}

    # Reguła do rozpoznawania tablicy z zakresami
    @_('declarations COMMA IDENTIFIER LTABPAREN index_range RTABPAREN')
    def declarations(self, p):
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

    @_('IF check THEN statements ELSE statements ENDIF')
    def statement(self, p):
        return {'type' : 'if', 'check' : p.check, 'body' : p.statements0, 'else' : p.statements1, 'lineno':p.lineno}


    @_('IF check THEN statements ENDIF')
    def statement(self, p):
        return {'type': 'if', 'check': p.check, 'body': p.statements, 'else': None, 'lineno':p.lineno}

    @_('WHILE check DO statements ENDWHILE')
    def statement(self, p):
        return {'type': 'loop', 'loop_type' : 'while', 'body': p.statements, 'lineno':p.lineno, 'check': p.check}

    @_('REPEAT statements UNTIL check SEMICOLON')
    def statement(self, p):
        return {'type': 'loop', 'loop_type' : 'repeat', 'body': p.statements, 'lineno':p.lineno, 'check': p.check}

    @_('FOR IDENTIFIER FROM factor DOWNTO factor DO statements ENDFOR')
    def statement(self, p):
        return {'type': 'loop', 'loop_type' : 'for', 'for_loop_type' : 'DOWNTO', 'body': p.statements, 'lineno':p.lineno, 'start': p.factor0, 'end': p.factor1, "iterator" : p.IDENTIFIER}

    @_('FOR IDENTIFIER FROM factor TO factor DO statements ENDFOR')
    def statement(self, p):
        return {'type': 'loop', 'loop_type' : 'for', 'for_loop_type' : 'TO', 'body': p.statements, 'lineno':p.lineno, 'start': p.factor0, 'end': p.factor1, "iterator" : p.IDENTIFIER}

    @_('statement')
    def statements(self, p):
        return [p.statement]


    @_('IDENTIFIER LTABPAREN expression RTABPAREN ASSIGN expression SEMICOLON')
    def statement(self, p):
        return {'type': 'assignment', 'variable': {"type": "variable", "name" : p.IDENTIFIER, 'lineno':p.lineno}, 'variable_type': 'table' ,'value': p.expression1, 'lineno':p.lineno, 'indeks' : p.expression0}



    # Przypisanie zmiennej
    @_('IDENTIFIER ASSIGN expression SEMICOLON')
    def statement(self, p):
        return {'type': 'assignment', 'variable': {"type": "variable", "name" : p.IDENTIFIER, 'lineno':p.lineno}, 'variable_type': 'variable' ,'value': p.expression, 'lineno':p.lineno}



    #PROC CALL
    @_('IDENTIFIER LPAREN args_call RPAREN SEMICOLON')
    def statement(self, p):
        return {"type": "proc_call", "name" : p.IDENTIFIER, "args": p.args_call, 'lineno':p.lineno}

    @_('IDENTIFIER LPAREN RPAREN SEMICOLON')
    def statement(self, p):
        return {"type": "proc_call", "name": p.IDENTIFIER, "args": [], 'lineno':p.lineno}

    @_('args_call COMMA IDENTIFIER')
    def args_call(self, p):
        return p.args_call + [{"type": "variable", "name" : p.IDENTIFIER, 'lineno':p.lineno}]

    @_('args_call COMMA T IDENTIFIER')
    def args_call(self, p):
        return p.args_call + [{"type": "table", "name": p.IDENTIFIER, 'lineno':p.lineno}]


    @_('T IDENTIFIER')
    def args_call(self, p):
        return [{"type": "table", "name": p.IDENTIFIER, 'lineno':p.lineno}]
    @_('IDENTIFIER')
    def args_call(self, p):
        return [{"type": "variable", "name" : p.IDENTIFIER, 'lineno':p.lineno}]
    #END PROC CALL

#LTABPAREN
    # Instrukcja odczytu
    @_('READ IDENTIFIER LTABPAREN MINUS NUMBER RTABPAREN SEMICOLON')
    def statement(self, p):

        return {'type': 'read', 'variable': {"type": "table", "name" : p.IDENTIFIER, 'indeks': -int(p.NUMBER), 'lineno':p.lineno}, 'lineno':p.lineno}

    @_('READ IDENTIFIER LTABPAREN NUMBER RTABPAREN SEMICOLON')
    def statement(self, p):

        return {'type': 'read', 'variable': {"type": "table", "name" : p.IDENTIFIER, 'indeks': int(p.NUMBER), 'lineno':p.lineno}, 'lineno':p.lineno}

    @_('READ IDENTIFIER SEMICOLON')
    def statement(self, p):

        return {'type': 'read', 'variable': {"type": "variable", "name" : p.IDENTIFIER, 'lineno':p.lineno}, 'lineno':p.lineno}

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

    @_('expression EQUAL expression')
    def check(self, p):
        return {'type': 'comparison', 'operator': '=', 'left': p.expression0, 'right': p.expression1,
                'lineno': p.lineno}

    @_('expression NOTEQUAL expression')
    def check(self, p):
        return {'type': 'comparison', 'operator': '!=', 'left': p.expression0, 'right': p.expression1,
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

    @_('term MOD factor')
    def term(self, p):
        return {'type': 'expression', 'left': p.term, 'operator': '%', 'right': p.factor, 'lineno': p.lineno}

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

    @_('IDENTIFIER LTABPAREN expression RTABPAREN')
    def factor(self, p):
        return {'type': 'identifier', 'name': p.IDENTIFIER, 'lineno': p.lineno, 'var_type': 'table', 'indeks': p.expression}

    @_('IDENTIFIER')
    def factor(self, p):
        return {'type': 'identifier', 'name': p.IDENTIFIER, 'lineno':p.lineno, 'var_type': 'var'}

    # Obsługa nawiasów
    @_('LPAREN expression RPAREN')
    def factor(self, p):
        return p.expression

    # Obsługa błędów składniowych
    def error(self, p):
        raise PerserError(p.lineno, f"cant proces {p.type} in this context")

