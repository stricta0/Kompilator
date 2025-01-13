class Systemic:
    def __init__(self, Variables, register):
        self.Variables = Variables
        self.register = register
        self.lineno = 0

    def read(self, statement):
        var = statement["variable"]
        comad = self.register.get_comand_var(var)
        return comad

    def write_var(self, var):
        comand = self.register.put_var(var)
        return comand

    def write_number(self, statement):
        value = statement["value"]
        comand = self.register.set_comand(value)
        comand += self.register.put_var("reg")
        return comand

    def assigment_var(self, left_var, right_var):
        comand = self.register.load_var(left_var)
        comand += self.register.store(right_var)
        return comand

    def assigment_number(self, left_var, number):
        comand = self.register.set_comand(number)
        comand += self.register.store(left_var)
        return comand

    def assigment_reg(self, var):
        comand = self.register.store(var)
        return comand
