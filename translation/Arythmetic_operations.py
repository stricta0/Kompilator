class ArythmeticOperations:
    def __init__(self, Variables, register):
        self.Variables = Variables
        self.register = register

    def add(self, left, right, left_token, right_token):
        comand = ""
        comand += left #calc left side
        line, x = self.register.store_helper_multiple_vars()
        comand += line
        comand += right #calc right side
        comand += self.register.add_var(x)
        return comand


    def sub(self, left, right, left_token, right_token):
        comand = ""
        comand += right #calc right side
        line, x = self.register.store_helper_multiple_vars()
        comand += line
        comand += left  # calc left side
        comand += self.register.sub_var(x)
        return comand

    def devide(self,left, right, left_token, right_token):
        if left_token['type'] == 'number' and right_token['type'] == 'number':
            comand = ""
            left_val = left_token['value']
            right_val = right_token['value']
            if right_val == 0:
                comand += self.register.load_var(self.register.zero_element)
                return comand
            resoult_of_multiple = left_val // right_val
            comand += self.register.set_comand(resoult_of_multiple)
            return comand  # Jesli mnozymy 2 liczby to nie ma co sie bawic - dzielimy na etapie kompilacji
        if right_token['type'] == 'number': #lewy token bedacy liczba za duzo nie daje
            right_val = right_token['value']
            comand = ""
            if right_val == 0:
                comand += self.register.load_var(self.register.zero_element)
                return comand
            is_negaitve = False
            if right_val < 0:
                right_val *= -1
                is_negaitve = True

            if self.is_power_of_2(right_val):
                comand += left  # wykonaj lewa strone
                while right_val > 1:
                    right_val = right_val // 2
                    comand += self.register.half()
                if is_negaitve:
                    comand += self.register.sub_var("0_reg")
                    comand += self.register.sub_var("0_reg")
                return comand
        #dzielenie zwykle juz w programie
        comand = ""
        comand += left  # oblicz lewa strone
        line, a = self.register.store_helper_multiple_vars()
        comand += line  # a = left_side
        comand += right
        line, b= self.register.store_helper_multiple_vars() #b = right side
        comand += line
        line, old_b = self.register.store_helper_multiple_vars() #old b = b
        comand += line
        comand += self.register.jzero(2) #if b == 0:
        comand += self.register.jump(3) #if b!= 0:
        comand += self.register.load_var(self.register.zero_element) # a // 0 = 0 (wedlug definicji programu nie matematyki)
        comand += self.register.marked_jump("END", "JUMP") #koniec! #was 36

        # wynik is ujemny
        comand += self.register.load_var(self.register.zero_element)
        line, wynik_is_ujemny = self.register.store_helper_multiple_vars()  # wynik_is_ujemny = 0
        comand += line
        comand += self.register.load_var(a)
        comand += self.register.jneg(2)
        comand += self.register.jump(6)
        comand += self.register.sub_var(a)
        comand += self.register.sub_var(a)
        comand += self.register.store(a) # a = -a
        comand += self.register.load_var(self.register.one_element)
        comand += self.register.store(wynik_is_ujemny) #set wynik is ujemny
        comand += self.register.load_var(b)
        comand += self.register.jneg(2)
        comand += self.register.jump(8)
        comand += self.register.sub_var(b)
        comand += self.register.sub_var(b)
        comand += self.register.store(b) # b = -b
        comand += self.register.store(old_b)
        comand += self.register.load_var(wynik_is_ujemny)
        comand += self.register.add_var(self.register.one_element)
        comand += self.register.store(wynik_is_ujemny)
        #end wynik is ujemny

        comand += self.register.load_var(self.register.zero_element)
        line, save_power = self.register.store_helper_multiple_vars() #save_power = 0
        comand += line
        power = self.register.create_var_but_dont_store() #stworz zmienna power ale nie dodawaj do comand
        #chcemy stworzyc ta zmienna ale na poczatku petli i tak trzeba ja ustawic na 1 wiec nie trzeba tego
        #robic teraz

        #poczatek petli
        comand += self.register.add_mark("Begin_loop")
        comand += self.register.load_var(self.register.one_element)
        comand += self.register.store(power) #power = 1
        comand += self.register.load_var(b) #reg = b
        comand += self.register.add_mark("Begin_1_loop")
        comand += self.register.sub_var(a) #reg = b - a
        #comand += self.register.jneg(8) #if b - a < 0 : kontunuuj petle
        comand += self.register.jneg(2)
        comand += self.register.marked_jump("End_1_loop", "JUMP")
        #cialo petli while b < a
        comand += self.register.load_var(power) #reg = power
        comand += self.register.add_var(power) #reg = 2power
        comand += self.register.store(power) #power = 2power

        comand += self.register.load_var(b) #reg = b
        comand += self.register.add_var(b) #reg = 2b
        comand += self.register.store(b) #b = 2b

        #comand += self.register.jump(-8) #wroc do poczatku petli
        comand += self.register.marked_jump("Begin_1_loop", "JUMP")
        comand += self.register.add_mark("End_1_loop")
        #koniec petli while b < a
        comand += self.register.load_var(b) # reg = b
        comand += self.register.sub_var(a) #reg = b - a
        comand += self.register.jzero(2) #if b == a
        comand += self.register.jump(4) #else
        comand += self.register.load_var(power) #reg = power
        comand += self.register.add_var(save_power) # reg = power + save_power
        comand += self.register.marked_jump("END", "JUMP") #end - koniec dzielenia
        comand += self.register.load_var(power)
        comand += self.register.half()
        comand += self.register.store(power) #power = power // 2
        comand += self.register.add_var(save_power) #reg = power + save_power
        comand += self.register.store(save_power) #save_power = power + save_power
        comand += self.register.load_var(b)
        comand += self.register.half()
        comand += self.register.store(b) # b = b // 2
        comand += self.register.load_var(a) #reg = a
        comand += self.register.sub_var(b) #reg = a - b
        comand += self.register.store(a) #a = a - b
        comand += self.register.load_var(old_b)
        comand += self.register.store(b) #b = old_b
        comand += self.register.sub_var(a) #reg = b - a
        comand += self.register.jpos(2) #if b > a - zakoncz program
        #comand += self.register.jump(-31) #else wroc do petli
        comand += self.register.marked_jump("Begin_loop", "JUMP")
        comand += self.register.load_var(save_power) #reg = save_power (wynik)
        comand += self.register.add_mark("END")



        #execute wynik is ujemny
        comand += self.register.store(save_power)
        comand += self.register.load_var(wynik_is_ujemny)
        comand += self.register.sub_var(self.register.one_element)
        #now wynik is ujemny = -1 v 0 v 1 - jesli wynik byl zerem to jest -1, jesli 2 to 1 a wiec tylko dla 0 zmieniamy znak
        comand += self.register.jzero(2)
        comand += self.register.jump(4)
        comand += self.register.load_var(self.register.zero_element)
        comand += self.register.sub_var(save_power)
        comand += self.register.store(save_power)

        comand += self.register.load_var(save_power)



        self.register.new_marks() #dont use the same markers next time
        return comand



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
                comand += self.register.load_var(self.register.zero_element)
                return comand
            if self.is_power_of_2(val): #Power of two multiple
                #Wiemy jaka liczba jest val wiec nawet nie potrzebujemy tego uwzgledniac w kodzie
                comand += right #Wykonaj prawa strone i zapisz w registerze
                while val != 1:
                    comand += self.register.add_var("0_reg")
                    val = val // 2
                if flip_resoult:
                    line, res = self.register.store_helper_multiple_vars()
                    comand += line
                    comand += self.register.sub_var(res)
                    comand += self.register.sub_var(res)
                return comand
            else:
                comand += self.register.load_var(self.register.zero_element) #load zero do registera
                line, wynik = self.register.store_helper_multiple_vars() #zapisz wynik = 0
                comand += line
                comand += right #oblicz prawa strone (lewa to nasze val)
                line, b = self.register.store_helper_multiple_vars() #zapisz b = right
                comand += line
                wynik_did_change = False
                while val != 0: #rosyjsie mnozenie chlopskie
                    if val == 1:
                        comand += self.register.add_var(wynik)
                        break
                    if val % 2 == 1: #reg = b
                        if wynik_did_change:
                            comand += self.register.add_var(wynik) #reg = b + wynik
                            comand += self.register.store(wynik) #wynik = reg (b + wynik)
                            comand += self.register.load_var(b) #reg = b
                        else:
                            comand += self.register.store(wynik)  # wynik = reg (b + wynik)
                            wynik_did_change = True
                    if val == 2 or val == 3:
                        comand += self.register.add_var(b)  # reg = b * 2
                        val = val // 2
                        continue
                    comand += self.register.add_var(b) #reg = b * 2
                    comand += self.register.store(b)
                    val = val // 2
                #comand += self.register.load_var_number(wynik)
                if flip_resoult:
                    comand += self.register.store(wynik)
                    comand += self.register.sub_var(wynik)
                    comand += self.register.sub_var(wynik)
                return comand
        else: #zadna z zmiennych nie jest liczba!
            comand = ""

            comand += self.register.load_var(self.register.zero_element) #pobierz 0
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
            comand += self.register.load_var(self.register.one_element)  # reg = 1
            comand += self.register.store(wynik_is_ujemny)  # wynik_is_ujemny = 1
            comand += self.register.load_var(self.register.zero_element) #reg = 0
            comand += self.register.sub_var(a) # a -a -a -> z ujemnej na dodatnia
            comand += self.register.store(a) #a = -a 3 ostatnie linijki

            #reg = a - poczatek petli
            comand += self.register.add_mark("BeginLop")
            comand += self.register.half() # reg = a//2
            comand += self.register.add_var("0_reg") # reg = a//2 + a//2
            comand += self.register.sub_var(a) #reg = a//2 * 2 - a #0 - parzyste, -1 nieparzyste
            comand += self.register.jzero(4) #jesli a%2 == 0 nie dodawaj do wyniku
            comand += self.register.load_var(wynik) #reg = wynik
            comand += self.register.add_var(b) #reg = wynik + b
            comand += self.register.store(wynik) #wynik = wynik + b
            comand += self.register.load_var(b) #reg = b
            comand += self.register.add_var(b) #reg = b*2
            comand += self.register.store(b) #b = b*2
            comand += self.register.load_var(a) #reg = a
            comand += self.register.half() #reg = a//2
            comand += self.register.store(a) #a = a//2
            #comand += self.register.jpos(-13) #jesli a>0 - wroc do poczatku petli
            comand += self.register.marked_jump("BeginLop", "JPOS")

            #comand += self.register.load_var_number(wynik) #reg = wynik
            comand += self.register.load_var(wynik_is_ujemny) #reg = wynik_is_ujemny
            comand += self.register.jzero(4)
            comand += self.register.load_var(self.register.zero_element)
            comand += self.register.sub_var(wynik) #0 - wynik = -wynik
            comand += self.register.jump(2)
            comand += self.register.load_var(wynik) # = wynik

            self.register.new_marks()
            return comand


    def is_power_of_2(self, x):
        wal = 1
        while wal <= x:
            if wal == x:
                return True
            wal = wal * 2
        return False

    def modulo(self, left, right, left_token, right_token):
        comand = ""
        comand += left  # oblicz lewa strone
        line, a = self.register.store_helper_multiple_vars()
        comand += line  # a = left_side
        comand += right
        line, b = self.register.store_helper_multiple_vars()  # b = right side
        comand += line
        line, old_b = self.register.store_helper_multiple_vars()  # old b = b
        comand += line
        comand += self.register.jzero(2)  # if b == 0:
        comand += self.register.jump(3)  # if b!= 0:
        comand += self.register.load_var(
            self.register.zero_element)  # a // 0 = 0 (wedlug definicji programu nie matematyki)
        comand += self.register.marked_jump("END", "JUMP")  # koniec! #was 36

        # wynik is ujemny
        comand += self.register.load_var(self.register.zero_element)
        line, wynik_is_ujemny = self.register.store_helper_multiple_vars()  # wynik_is_ujemny = 0
        comand += line
        comand += self.register.load_var(a)
        comand += self.register.jneg(2)
        comand += self.register.jump(4) #was 6
        comand += self.register.sub_var(a)
        comand += self.register.sub_var(a)
        comand += self.register.store(a)  # a = -a
        #comand += self.register.load_var(self.register.one_element)
        #comand += self.register.store(wynik_is_ujemny)  # set wynik is ujemny
        comand += self.register.load_var(b)
        comand += self.register.jneg(2)
        comand += self.register.jump(8)
        comand += self.register.sub_var(b)
        comand += self.register.sub_var(b)
        comand += self.register.store(b)  # b = -b
        comand += self.register.store(old_b)
        comand += self.register.load_var(wynik_is_ujemny)
        comand += self.register.add_var(self.register.one_element)
        comand += self.register.store(wynik_is_ujemny)
        # end wynik is ujemny

        comand += self.register.load_var(a)
        comand += self.register.sub_var(b) # if a - b < 0: return a
        comand += self.register.jneg(2)
        comand += self.register.jump(3)
        comand += self.register.load_var(a)
        comand += self.register.marked_jump("END", "JUMP")





        comand += self.register.load_var(self.register.zero_element)
        line, save_power = self.register.store_helper_multiple_vars()  # save_power = 0
        comand += line
        power = self.register.create_var_but_dont_store()  # stworz zmienna power ale nie dodawaj do comand
        # chcemy stworzyc ta zmienna ale na poczatku petli i tak trzeba ja ustawic na 1 wiec nie trzeba tego
        # robic teraz

        # poczatek petli
        comand += self.register.add_mark("Begin_loop")
        comand += self.register.load_var(self.register.one_element)
        comand += self.register.store(power)  # power = 1
        comand += self.register.load_var(b)  # reg = b
        comand += self.register.add_mark("Begin_1_loop")
        comand += self.register.sub_var(a)  # reg = b - a
        # comand += self.register.jneg(8) #if b - a < 0 : kontunuuj petle
        comand += self.register.jneg(2)
        comand += self.register.marked_jump("End_1_loop", "JUMP")
        # cialo petli while b < a
        comand += self.register.load_var(power)  # reg = power
        comand += self.register.add_var(power)  # reg = 2power
        comand += self.register.store(power)  # power = 2power

        comand += self.register.load_var(b)  # reg = b
        comand += self.register.add_var(b)  # reg = 2b
        comand += self.register.store(b)  # b = 2b

        # comand += self.register.jump(-8) #wroc do poczatku petli
        comand += self.register.marked_jump("Begin_1_loop", "JUMP")
        comand += self.register.add_mark("End_1_loop")
        # koniec petli while b < a
        comand += self.register.load_var(b)  # reg = b
        comand += self.register.sub_var(a)  # reg = b - a
        comand += self.register.jzero(2)  # if b == a
        comand += self.register.jump(4)  # else
        comand += self.register.load_var(a)  # reg = power
        comand += self.register.sub_var(b)  # reg = power + save_power
        comand += self.register.marked_jump("END", "JUMP")  # end - koniec dzielenia
        comand += self.register.load_var(power)
        comand += self.register.half()
        comand += self.register.store(power)  # power = power // 2
        comand += self.register.add_var(save_power)  # reg = power + save_power
        comand += self.register.store(save_power)  # save_power = power + save_power
        comand += self.register.load_var(b)
        comand += self.register.half()
        comand += self.register.store(b)  # b = b // 2
        comand += self.register.load_var(a)  # reg = a
        comand += self.register.sub_var(b)  # reg = a - b
        comand += self.register.store(a)  # a = a - b
        comand += self.register.load_var(old_b)
        comand += self.register.store(b)  # b = old_b
        comand += self.register.sub_var(a)  # reg = b - a
        comand += self.register.jpos(2)  # if b > a - zakoncz program
        # comand += self.register.jump(-31) #else wroc do petli
        comand += self.register.marked_jump("Begin_loop", "JUMP")
        comand += self.register.load_var(a)  # reg = save_power (wynik)
        comand += self.register.add_mark("END")

        # execute wynik is ujemny
        comand += self.register.store(save_power)
        comand += self.register.load_var(wynik_is_ujemny)
        #comand += self.register.sub_var(self.register.one_element)
        # tutaj wynik is ujemny  = 1 lub 0 - gdzie 1 ozancza odwroc znak
        comand += self.register.jpos(2) #was jzero
        comand += self.register.jump(4)
        comand += self.register.load_var(self.register.zero_element)
        comand += self.register.sub_var(save_power)
        comand += self.register.store(save_power)

        comand += self.register.load_var(save_power)
        self.register.new_marks()  # dont use the same markers next time
        return comand
