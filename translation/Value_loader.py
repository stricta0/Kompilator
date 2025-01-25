from translation import ArythmeticComparision, ArythmeticOperations

class ValueLoader:
    def __init__(self, Variables, register, arytmetic, systemic):
        self.Variables = Variables
        self.register = register
        self.operations = ArythmeticOperations(self.Variables, self.register)
        self.comparision = ArythmeticComparision(self.Variables, self.register)
        self.arytmetic = arytmetic
        self.systemic = systemic


    def save_value_from_statement_in_reg(self, statement):  # save statment in reg

        if statement["type"] == "identifier":
            if statement["var_type"] == "var":
                return self.register.load_var(statement["name"])
            if statement["var_type"] == "table":
                comand = self.save_value_from_statement_in_reg(statement["indeks"])
                return comand + self.systemic.load_tab_i(statement['name'])
        if statement["type"] == "number":
            return self.register.set_comand(statement["value"])
        if statement["type"] == "expression":
            return self.arytmetic.solve_expression(statement)
        if statement["type"] == "comparison":
            return self.arytmetic.solve_comparison(statement)

