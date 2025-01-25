class Systemic:
    def __init__(self, Variables, register):
        self.Variables = Variables
        self.register = register
        self.lineno = 0

    def read(self, statement):
        var = statement["variable"]
        comand = self.register.get_comand(var)
        return comand

    def write_var(self, var):
        comand = self.register.put_var(var)
        return comand

    def write_number(self, statement):
        value = statement["value"]
        comand = self.register.set_comand(value)
        comand += self.register.put_var("reg")
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

        line, self.Variables[tab_name] = self.register.store_helper_multiple_vars()  #tab_name przechowuje start indeks tablicy

        comand += line #self.Variabels[tab_name] = start
        comand += self.register.set_comand(self.Variables[tab_name] + 2) #ten jest +1 - kolejny - czyli pierwszy w tablicy - +2 #reg = indeks pierwszego elementu tablicy (przyda sie zamiast seta robic za kazdym razem bo jest drozszy)
        comand += self.register.add(self.Variables[tab_name]) #new
        comand += self.register.store(tab_name) #new| tab_name przechowuje wartości -> -start + adres tab[0]
        #line, tab_0 = self.register.store_helper_multiple_vars()
        #comand += line
        for i in range(start, end+1):
            self.register.create_var_but_dont_store() #zarezewruj miejsce w pamieci dla zmienneych taba

        return comand

    #get statement of varible of type variable_type (tab[3] for example)
    #and returns real indeks of tab[3] in vm
    def get_real_table_variable_indeks(self, tab_name): #reg = i
        indeks_of_element_with_start_val = self.Variables[tab_name]
        #indeks_zero = indeks_of_element_with_start_val + 1  # indeks pierwszego elememntu tablicy (tab[0])
        comand = ""
        comand += self.register.add(indeks_of_element_with_start_val)  # reg = i - start
        #comand += self.register.add(indeks_zero)  # reg = i - start + adres_tab[0] - mam nadzieje ze dziala xd
        return comand

    #assume - reg = i
    def store_tab_addres_in__helper(self, tab_name):
        comand = self.get_real_table_variable_indeks(tab_name)
        line, helper = self.register.store_helper_multiple_vars()
        comand += line
        #comand += self.register.store("_helper")
        return comand, helper

    def load_tab_i(self, tab_name): #LOAD
        comand, helper = self.store_tab_addres_in__helper(tab_name)
        comand += self.register.load_i_var_number(helper)
        return comand