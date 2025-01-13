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

    def create_tab(self, tab_name, start, end, line):
        if start > end:
            raise ValueError(f"at line {line.lineno}, cant create tab with start < end!")

        comand  = ""
        comand += self.register.set_comand(start)

        line, self.Variables[tab_name] = self.register.store_helper_multiple_vars()  #tab_name przechowuje start indeks tablicy
        comand += line
        for i in range(start, end+1):
            self.Variables['number_of_vars'] += 1 #zarezerwuj zmienna

    def get_val_from_tab(self, tab_name, i):
        indeks_of_first_indeks = self.Variables[tab_name] #ideks obiektu przechowujacego rozmiar tablicy
        compand = ""
        compand += self.register.load_var_number(indeks_of_first_indeks) #reg = start_tablicy
        compand += self.register.sub()