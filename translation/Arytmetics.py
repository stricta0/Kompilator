from idlelib.autocomplete import completion_kwds


class Arytmetic:
    def __init__(self, Variables, register):
        self.Variables = Variables
        self.register = register
        self.lineno = 0

    def value_loader(self, value):
        right = ""
        if value['type'] == 'expression':
            right = self.solve_expression(value)
        elif value['type'] == "number":
            print("HERE WE USE SET COMAND")
            right = self.register.set_comand(value['value'])
        elif value['type'] == "identifier":
            right = self.register.load_var(value['name'])
        return right
    #seve left to register
    #operatio n right to register
    #leave resoult in register
    def solve_expression(self, expresion):
        print("Rozpoczeto slove_expresion")
        left = expresion['left']
        left_part = self.value_loader(left)
        right = expresion['right']
        right_part = self.value_loader(right)
        operation = expresion['operator']
        if operation == "+":
            return self.add(left_part, right_part, left, right)
        if operation == "-":
            return self.sub(left_part, right_part, left, right)
        if operation == "%":
            pass
        if operation == "/":
            pass
        if operation == "*":
            print("wykryto *")
            return self.multiple(left_part, right_part, left, right)



    def add(self, left, right, left_token, right_token):
        #Run left side, save in variable, run right side (stays in register) then add the left side var
        comand = ""

        #If left side is just a var there is no need to save load and save it somewere else
        if left_token['type'] == 'identifier':
            self.register.check_if_variable_exists(left_token['name'])
            x = self.Variables[left_token['name']]
        else:
            comand += left #calc left side
            line, x = self.register.store_helper_multiple_vars()
            comand += line #save reg in x


        comand += right #calc right side
        #comand += f"ADD {x}\n"#add left side to right side
        comand += self.register.add(x)
        return comand


    def sub(self, left, right, left_token, right_token):
        comand = ""
        #line, x = self.register.store_helper_multiple_vars()

        if right_token['type'] == 'identifier':
            self.register.check_if_variable_exists(right_token['name'])
            x = self.Variables[right_token['name']]
        else:
            comand += right #calc right side
            line, x = self.register.store_helper_multiple_vars()
            comand += line #save reg in x

        comand += left  # calc left side
        #comand += f"SUB {x}\n"  # add left side to right side
        comand += self.register.sub(x)
        return comand

    def devide(self, left, right):
        pass
    def devide_helper(self, x, y):
        pass
    def multiple(self,left, right, left_token, right_token):
        comand = ""
        if left_token['type'] == 'number' and right_token['type'] == 'number':
            left_val = left_token['value']
            right_val = right_token['value']

            resoult_of_multiple = left_val * right_val
            comand += self.register.set_comand(resoult_of_multiple)
            return comand #Jesli mnozymy 2 liczby to nie ma co sie bawic - mnozymy na etapie kompilacji
        if left_token['type'] == 'number' or right_token['type'] == 'number':
            if left_token['type'] != 'number':
                left_token, right_token, left, right = right_token, left_token, right, left #zamien miejscami tak aby zawsze po lewiej byla liczba

            #Wykonaj prawa strone
            val = left_token['value']
            flip_resoult = False
            if val < 0:
                flip_resoult = True
                val = val * -1
            if val == 0: #jesli wartosc to zero to zaladuj 0
                comand += self.register.make_0_and_1_if_dont_exist_already()
                comand += self.register.load_var_number(self.register.zero_indeks)
                return comand
            if self.is_power_of_2(val): #Power of two multiple
                #Wiemy jaka liczba jest val wiec nawet nie potrzebujemy tego uwzgledniac w kodzie
                comand += right #Wykonaj prawa strone i zapisz w registerze
                while val != 1:
                    comand += self.register.add(0)
                    val = val // 2
                if flip_resoult:
                    line, res = self.register.store_helper_multiple_vars()
                    comand += line
                    comand += self.register.sub(res)
                    comand += self.register.sub(res)
                return comand
            else:
                comand += self.register.make_0_and_1_if_dont_exist_already() #stworz zero jak nie istnieje
                comand += self.register.load_var_number(self.register.zero_indeks) #load zero do registera
                line, wynik = self.register.store_helper_multiple_vars() #zapisz wynik = 0
                comand += line
                comand += right #oblicz prawa strone (lewa to nasze val)
                line, b = self.register.store_helper_multiple_vars() #zapisz b = right
                comand += line
                wynik_did_change = False
                while val != 0: #rosyjsie mnozenie chlopskie
                    if val == 1:
                        comand += self.register.add(wynik)
                        break
                    if val % 2 == 1: #reg = b
                        if wynik_did_change:
                            comand += self.register.add(wynik) #reg = b + wynik
                            comand += self.register.store_number_var(wynik) #wynik = reg (b + wynik)
                            comand += self.register.load_var_number(b) #reg = b
                        else:
                            comand += self.register.store_number_var(wynik)  # wynik = reg (b + wynik)
                            wynik_did_change = True
                    if val == 2 or val == 3:
                        comand += self.register.add(b)  # reg = b * 2
                        val = val // 2
                        continue
                    comand += self.register.add(b) #reg = b * 2
                    comand += self.register.store_number_var(b)
                    val = val // 2
                #comand += self.register.load_var_number(wynik)
                if flip_resoult:
                    comand += self.register.store_number_var(wynik)
                    comand += self.register.sub(wynik)
                    comand += self.register.sub(wynik)
                return comand
        else: #zadna z zmiennych nie jest liczba!
            comand = ""

            comand += self.register.make_0_and_1_if_dont_exist_already() #dodaj 0 i 1 jak nie ma
            comand += self.register.load_var_number(self.register.zero_indeks) #pobierz 0
            line, wynik = self.register.store_helper_multiple_vars() #wynik = 0
            comand += line
            line, wynik_is_ujemny = self.register.store_helper_multiple_vars() #wynik_is_ujemny = 0
            comand += line

            comand += right  # Wykonaj prawa strone
            line, b = self.register.store_helper_multiple_vars()
            comand += line

            comand += left  # Wynokaj lewa strone
            line, a = self.register.store_helper_multiple_vars()
            comand += line
            #Aktualnie reg = a
            # Obliczono left i right i dodano do zmiennych a i b, teraz wykonaj mnozenie a * b
            comand += self.register.jneg(2) #jak a jest ujemne to napraw to
            comand += self.register.jump(6) #a jak nie jest to nie
            comand += self.register.load_var_number(self.register.one_indeks)  # reg = 1
            comand += self.register.store_number_var(wynik_is_ujemny)  # wynik_is_ujemny = 1
            comand += self.register.load_var_number(self.register.zero_indeks) #reg = 0
            comand += self.register.sub(a) # a -a -a -> z ujemnej na dodatnia
            comand += self.register.store_number_var(a) #a = -a 3 ostatnie linijki

            #reg = a - poczatek petli
            comand += self.register.half() # reg = a//2
            comand += self.register.add(0) # reg = a//2 + a//2
            comand += self.register.sub(a) #reg = a//2 * 2 - a #0 - parzyste, -1 nieparzyste
            comand += self.register.jzero(4) #jesli a%2 == 0 nie dodawaj do wyniku
            comand += self.register.load_var_number(wynik) #reg = wynik
            comand += self.register.add(b) #reg = wynik + b
            comand += self.register.store_number_var(wynik) #wynik = wynik + b
            comand += self.register.load_var_number(b) #reg = b
            comand += self.register.add(b) #reg = b*2
            comand += self.register.store_number_var(b) #b = b*2
            comand += self.register.load_var_number(a) #reg = a
            comand += self.register.half() #reg = a//2
            comand += self.register.store_number_var(a) #a = a//2
            comand += self.register.jpos(-13) #jesli a>0 - wroc do poczatku petli

            #comand += self.register.load_var_number(wynik) #reg = wynik
            comand += self.register.load_var_number(wynik_is_ujemny) #reg = wynik_is_ujemny
            comand += self.register.jzero(4)
            comand += self.register.load_var_number(self.register.zero_indeks)
            comand += self.register.sub(wynik) #0 - wynik = -wynik
            comand += self.register.jump(2)
            comand += self.register.load_var_number(wynik) # = wynik

            return comand






        return "ERROR? CO NA TYM MNOZENIU NIE POSZLO\n"





        # comand = ""
        # comand += left #calc left side and save in reg
        # line, w = self.register.store_helper_multiple_vars() #save left side in w
        # comand += line
        #
        # comand += right
        # line, x = self.register.store_helper_multiple_vars() #save right side in x
        # comand += line
        #
        # line, z = self.register.store_helper_multiple_vars()
        # comand += line #Save 0 as z value
        #
        #
        #
        #  #calc right side and store in reg

    def is_power_of_2(self, x):
        wal = 1
        while wal <= x:
            if wal == x:
                return True
            wal = wal * 2
        return False

    def modulo(self, left, right, left_token, right_token):
        comand = ""
        if left_token['type'] == 'number' and right_token['type'] == 'number':
            left_val = left_token['value']
            right_val = right_token['value']

            if right_val == 0:
                comand += self.register.make_0_and_1_if_dont_exist_already()
                comand += self.register.load_var_number(self.register.zero_indeks)
            else:
                resoult_of_mod = left_val % right_val
                comand += self.register.set_comand(resoult_of_mod)
            return comand  # Jesli mnozymy 2 liczby to nie ma co sie bawic - mod na etapie kompilacji
        if left_token['type'] == 'number' or right_token['type'] == 'number':
            if left_token['type'] == 'number':
                pass
            else: #right_token == number
                pass