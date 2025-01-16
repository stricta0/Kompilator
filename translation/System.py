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

    def create_tab(self, tab_name, start, end, lineno):
        if start > end:
            raise ValueError(f"at line {lineno}, cant create tab with start < end!")

        comand  = ""
        comand += self.register.set_comand(start) #reg = start

        line, self.Variables[tab_name] = self.register.store_helper_multiple_vars()  #tab_name przechowuje start indeks tablicy
        comand += line #self.Variabels[tab_name] = start
        comand += self.register.set_comand(self.Variables[tab_name] + 2) #ten jest +1 - kolejny - czyli pierwszy w tablicy - +2 #reg = indeks pierwszego elementu tablicy (przyda sie zamiast seta robic za kazdym razem bo jest drozszy)
        line, tab_0 = self.register.store_helper_multiple_vars()
        comand += line
        for i in range(start, end+1):
            self.register.create_var_but_dont_store() #zarezewruj miejsce w pamieci dla zmienneych taba

    def get_val_from_tab(self, tab_name, statement):
        indeks_of_element_with_start_val = self.Variables[tab_name]
        indeks_zero = indeks_of_element_with_start_val + 1 #indeks pierwszego elememntu tablicy (tab[0])
        comand = ""
        #comand += self.register.load_var_number(indeks_of_element_with_start_val) #reg = start
        i = None
        if statement['type'] == 'number':
            i = statement['value']
            comand += self.register.set_comand(i) #reg = i

        elif statement['type'] == 'variable':
            i_var = statement["name"] #nazwa zmiennej przechowujace i
            comand += self.register.load_var(i_var) #zaladuj i ze zmiennej


        else:
            raise ValueError(f"get_val_from_tab in System.py got value: {statement} wich is nor number nor variable")

        comand += self.register.sub(indeks_of_element_with_start_val)  # reg = i - start
        comand += self.register.add(indeks_zero)  # reg = i - start + adres_tab[0] - mam nadzieje ze dziala xd
        # teraz mamy w reg np. wartosc 12 i musimy zrobic LOAD 12
        comand += self.register.load_i_var_number(0)  # reg = p_ind_w_pamieci
        # jesli wszystko poszlo dobrze: reg = tab[i]
        return comand