from sly import Parser, Lexer
from Gramar import CalcLexer
from Gramar import GF1234577

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('left', POWER)
    )

    def __init__(self):
        self.postfix = []  # Lista do przechowywania wyniku w ONP

    def is_number(self, number_str):
        for letter in number_str:
            if not (ord("0") <= ord(letter) <= ord("9")):
                return False
        return True

    def change_postfix_to_group_numbers(self):
        for i in range(len(self.postfix)):
            if self.is_number(self.postfix[i]):
                self.postfix[i] = GF1234577(int(self.postfix[i]))
            elif len(self.postfix[i]) > 1:
                if self.postfix[i][0] == "-" and self.is_number(self.postfix[i][1:]):
                    self.postfix[i] = GF1234577(-1 * int(self.postfix[i][1:]))
    #Function IS NOT responsible for returning errors - if everything is wrote corectly this should NEVER return negative
    #number - we have some error returns just in case (so we dont get runtime error)
    def count_res(self):
        stos = []
        i = 0
        operations = ['+', '-', '*', ':', '^']
        while i <= len(self.postfix):
            if i == len(self.postfix):
                if len(stos) == 1:
                    return stos[0]
                elif len(stos) > 1:
                    return -3 # Tu much numbers
                else:
                    return -4 #not enough numburs

            if self.postfix[i] in operations:
                if len(stos) < 2:
                    return -1 #Error not enought numbers
            if self.postfix[i] == '+':
                stos.append(stos.pop() + stos.pop())
            elif self.postfix[i] == '-':
                stos.append(stos.pop() - stos.pop())
            elif self.postfix[i] == '*':
                stos.append(stos.pop() * stos.pop())
            elif self.postfix[i] == ':':
                a = stos.pop()
                b = stos.pop()
                try:
                    stos.append(b / a)
                except Exception as e:
                    raise e
            elif self.postfix[i] == '^':
                a = stos.pop()
                b = stos.pop()
                stos.append(b ** a)
            else:
                if isinstance(self.postfix[i], GF1234577):
                    stos.append(self.postfix[i])
                else:
                    return -2 #Error - unknown operation
            i += 1
        return -5 #While ended

    def get_resoult(self):
        return self.postfix


    @_('expr PLUS term')
    @_('expr MINUS term')
    def expr(self, p):
        self.postfix.append(p[1])  # Dodaj operator do ONP
        return f"{p.expr} {p.term} {p[1]}"





    @_('term')
    def expr(self, p):
        return p.term

    @_('term TIMES factor')
    @_('term DIVIDE factor')
    def term(self, p):
        self.postfix.append(p[1])
        return f"{p.term} {p.factor} {p[1]}"

    @_('factor POWER factor')
    def term(self, p):
        self.postfix.append(p[1])  # Dodaj operator '^' do ONP
        return f"{p.factor0} {p.factor1} {p[1]}"

    # Obsługuje przypadek, w którym operator występuje bez prawego operand
    @_('expr PLUS')
    @_('expr MINUS')
    @_('expr TIMES')
    @_('expr DIVIDE')
    @_('expr POWER')
    def expr(self, p):
        raise ValueError(f"Error: Operator '{p[1]}' missing right operand")

    # Obsługuje przypadek, w którym operator występuje bez lewego operand
    @_('PLUS expr')
    @_('MINUS expr')
    @_('TIMES expr')
    @_('DIVIDE expr')
    @_('POWER expr')
    def expr(self, p):
        raise ValueError(f"Error: Operator '{p[1]}' missing left operand")

    @_('factor')
    def term(self, p):
        return p.factor

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr


    @_('NUMBER')
    def factor(self, p):
        self.postfix.append(p.NUMBER)
        return p.NUMBER

    @_('NUMBER NUMBER')
    def factor(self, p):
        raise ValueError(f"Was given 2 numbers in a row - not a arithmetical operation")

    @_('NEGATIVE')
    def factor(self, p):
        self.postfix.append(p.NEGATIVE)
        return p.NEGATIVE

    @_('NEGATIVE NEGATIVE')
    def factor(self, p):
        raise ValueError(f"Was given 2 numbers in a row - not a arithmetical operation")



