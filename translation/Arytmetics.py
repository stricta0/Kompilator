from translation import ArythmeticComparision, ArythmeticOperations
class Arytmetic:
    def __init__(self, Variables, register, systemic):
        self.Variables = Variables
        self.register = register
        self.operations = ArythmeticOperations(self.Variables, self.register)
        self.comparision = ArythmeticComparision(self.Variables, self.register)
        self.systemic = systemic
        #self.lineno = 0

    def value_loader(self, value):
        right = ""
        if value['type'] == 'expression':
            right = self.solve_expression(value)
        elif value['type'] == "number":
            right = self.register.set_comand(value['value'])
        elif value['type'] == "identifier":
            self.register.check_if_initialize(value["name"], value["lineno"])
            if value['var_type'] == "table":
                right = self.value_loader(value["indeks"])
                right += self.systemic.load_tab_i(value['name'])
            else:
                right = self.register.load_var(value['name'])
        elif value['type'] == "comparison":
            right = self.solve_comparison(value)
        return right
    #seve left to register
    #operatio n right to register
    #leave resoult in register
    def solve_expression(self, expresion):
        left = expresion['left']
        left_part = self.value_loader(left)
        right = expresion['right']
        right_part = self.value_loader(right)
        operation = expresion['operator']
        if operation == "+":
            return self.operations.add(left_part, right_part, left, right)
        if operation == "-":
            return self.operations.sub(left_part, right_part, left, right)
        if operation == "%":
            return self.operations.modulo(left_part, right_part, left, right)
        if operation == "/":
            return self.operations.devide(left_part, right_part, left, right)
        if operation == "*":
            return self.operations.multiple(left_part, right_part, left, right)

    #returns True or False (reg = 1 - true, reg = 0 -> false)
    def solve_comparison(self, comparision_statment):
        comand = ""
        right = self.value_loader(comparision_statment["right"])
        comand += right #reg = right
        line, right_val = self.register.store_helper_multiple_vars()
        comand += line #right_val = right
        left = self.value_loader(comparision_statment["left"]) #reg = left
        comand += left
        comand += self.register.sub_var(right_val) #reg = left - right
        comand += self.comparision.comparison_type_solve(comparision_statment["operator"])
        return comand

    def custom_comparisone_of_vars(self, var1, var2, comparisone_type):
        comand = ""
        self.register.check_if_variable_exists(var1)
        self.register.check_if_variable_exists(var2)
        comand += self.register.load_var(var1)
        comand += self.register.sub_var(var2)
        comand += self.comparision.comparison_type_solve(comparisone_type)
        return comand



