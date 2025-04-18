class Systemic:
    def __init__(self, Variables, register):
        self.Variables = Variables
        self.register = register
        self.lineno = 0

    def read(self, statement):
        var = statement["variable"]["name"]
        comand = self.register.get_comand(var)
        return comand

    def write_var(self, var):
        comand = self.register.put_var(var)
        return comand

    def write_number(self, statement):
        value = statement["value"]
        comand = self.register.set_comand(value)
        comand += self.register.put_var("0_reg")
        return comand

    #we assume that reg = i
    # def tab_assigment(self, table_line):
    #     i = table_line["indeks"]
    #     if i["type"]


    def assigment_var(self, left_var, right_var):
        comand = self.register.load_var(right_var)
        comand += self.register.store(left_var)
        return comand

    def assigment_number(self, left_var, number):
        comand = self.register.set_comand(number)
        comand += self.register.store(left_var)
        return comand

    def assigment_reg(self, var):
        comand = self.register.store(var)
        return comand


    def create_tab(self, tab_name, start, end, lineno):
        if start > end:
            raise ValueError(f"at line {lineno}, cant create tab with start < end!")

        comand  = ""
        comand += self.register.set_comand(-start) #reg = start

        line, help_= self.register.store_helper_multiple_vars()  #tab_name przechowuje start indeks tablicy
        self.Variables[tab_name] = self.Variables[help_]
        comand += line #self.Variabels[tab_name] = start
        comand += self.register.set_comand(self.Variables[tab_name] + 2) #ten jest +1 - kolejny - czyli pierwszy w tablicy - +2 #reg = indeks pierwszego elementu tablicy (przyda sie zamiast seta robic za kazdym razem bo jest drozszy)
        comand += self.register.add_var(tab_name) #new
        comand += self.register.store(tab_name) #new| tab_name przechowuje wartości -> -start + adres tab[0]
        for i in range(start, end+2):
            self.register.create_var_but_dont_store() #zarezewruj miejsce w pamieci dla zmienneych taba

        return comand

    def create_tab_in_procedure(self, tab_name, start, end, lineno):
        if start > end:
            raise ValueError(f"at line {lineno}, cant create tab with start < end!")

        comand  = ""
        comand += self.register.set_comand(-start) #reg = start

        line, help_= self.register.store_helper_multiple_vars()  #tab_name przechowuje start indeks tablicy
        self.Variables[tab_name] = self.Variables[help_]
        comand += line #self.Variabels[tab_name] = start
        comand += self.register.set_comand(self.Variables[tab_name] + 2) #ten jest +1 - kolejny - czyli pierwszy w tablicy - +2 #reg = indeks pierwszego elementu tablicy (przyda sie zamiast seta robic za kazdym razem bo jest drozszy)
        comand += self.register.add_var(tab_name) #new
        comand += self.register.store(tab_name) #new| tab_name przechowuje wartości -> -start + adres tab[0]
        for i in range(start, end+2):
            self.register.create_var_but_dont_store() #zarezewruj miejsce w pamieci dla zmienneych taba
        tab_name_var = self.Variables[tab_name]
        self.Variables.pop(tab_name)
        return comand, tab_name_var

    #get statement of varible of type variable_type (tab[3] for example)
    #and returns real indeks of tab[3] in vm
    def get_real_table_variable_indeks(self, tab_name): #reg = i
        comand = ""
        comand += self.register.add_var(tab_name)  # reg = i - start
        return comand

    #assume - reg = i
    def store_tab_addres_in__helper(self, tab_name):
        comand = self.get_real_table_variable_indeks(tab_name)
        line, helper = self.register.store_helper_multiple_vars()
        comand += line
        return comand, helper

    def load_tab_i(self, tab_name): #LOAD
        comand, helper = self.store_tab_addres_in__helper(tab_name)
        comand += self.register.load_i_var(helper)
        return comand