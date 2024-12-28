class Arytmetic:
    def __init__(self, Variables, register):
        self.Variables = Variables
        self.register = register

    def assigment(self, statement):
        var = statement["variable"]
        if var not in self.Variables:
            return f"ERROR - variable {var} used but never created"
        value = statement["value"]
        right = self.value_loader(value)

        return f"{right}\nSTORE {self.Variables[var]}\n"


    def value_loader(self, value):
        right = ""
        if value['type'] == 'expression':
            right = self.solve_expression(value)
        elif value['type'] == "number":
            right = self.register.set_comand(value['value'])
        elif value['type'] == "identifier":
            right = self.register.load_var(value['name'])
        return right
    #seve left to register
    #operatio n right to register
    #leave resoult in register
    def solve_expression(self, expresion):
        print("solve expresion\n")
        left = expresion['left']
        print(left)
        left_part = self.value_loader(left)
        print(left_part)
        right = expresion['right']
        print(right)
        right_part = self.value_loader(right)
        print(right_part)
        operation = expresion['operator']
        if operation == "+":
            print("add operation")
            return self.add(left_part, right_part)
        if operation == "-":
            pass
        if operation == "%":
            pass
        if operation == "/":
            pass
        if operation == "*":
            pass



    def add(self, left, right):
        return f"{left}{self.register.store_helper()}{right}ADD {self.Variables['first_empty']}\n"
    def sub(self, left, right):
        return f"{left}{self.register.store_helper()}{right}SUB {self.Variables['first_empty']}\n"
    def devide(self, left, right):
        pass
    def multiple(self, left, right):
        pass
    def modulo(self, left, right):
        pass