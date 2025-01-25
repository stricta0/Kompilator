class ArythmeticComparision:
    def __init__(self, Variables, register):
        self.Variables = Variables
        self.register = register

    def comparison_type_solve(self, comp_type):
        if comp_type == "=":
            return self.equal()
        if comp_type == "!=":
            return self.not_equal()
        if comp_type == ">":
            return self.more_than()
        if comp_type == "<":
            return self.less_than()
        if comp_type == ">=":
            return self.more_or_equal()
        if comp_type == "<=":
            return self.less_or_equal()


    #reg = a-b now check if a==b
    def equal(self):
        comand = self.register.jzero(3)
        comand += self.register.load_var_number(self.register.zero_indeks)
        comand += self.register.jump(2)
        comand += self.register.load_var_number(self.register.one_indeks)
        return comand

    def not_equal(self):
        comand = self.register.jzero(3)
        comand += self.register.load_var_number(self.register.one_indeks)
        comand += self.register.jump(2)
        comand += self.register.load_var_number(self.register.zero_indeks)
        return comand

    def more_than(self):
        comand = self.register.jpos(3)
        comand += self.register.load_var_number(self.register.zero_indeks)
        comand += self.register.jump(2)
        comand += self.register.load_var_number(self.register.one_indeks)
        return comand

    def less_than(self):
        comand = self.register.jneg(3)
        comand += self.register.load_var_number(self.register.zero_indeks)
        comand += self.register.jump(2)
        comand += self.register.load_var_number(self.register.one_indeks)
        return comand

    def more_or_equal(self):
        comand = self.register.jneg(3)
        comand += self.register.load_var_number(self.register.one_indeks)
        comand += self.register.jump(2)
        comand += self.register.load_var_number(self.register.zero_indeks)
        return comand

    def less_or_equal(self):
        comand = self.register.jpos(3)
        comand += self.register.load_var_number(self.register.one_indeks)
        comand += self.register.jump(2)
        comand += self.register.load_var_number(self.register.zero_indeks)
        return comand




