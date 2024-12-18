from translation import Arytmetic, Systemic, Register

class Translator:

    def __init__(self, string_to_translate):
        self.text = string_to_translate
        #This dic has var_name : i, where i is indeks of this var in end code,
        #only execption is Variables["reg"] witch contains a var thats currently in register
        #and infor if it was changed thruout the program
        self.Variables = {}
        self.Variables["help"] = 1
        self.decripted = ""
        self.register = Register()

    def translate(self):
        self.declaration(self.text["declarations"])
        self.decripted = self.text

    def print(self):
        print("Input: ")
        print(self.text)
        print("\n\nOutput: ")
        print(self.decripted)

    def declaration(self, variabouls):
        i = 1
        for var in variabouls:
            self.Variables[var] = i
            i += 1
        self.Variables["help"] = i

    def statements(self):
        arytmetic = Arytmetic(self.Variables, self.register)
        systemic = Systemic(self.Variables, self.register)
        for statement in self.text["statements"]:
            if statement["type"] == "read":
                line = systemic.read(statement)
                continue
            if statement["type"] == "assignment":
                line = arytmetic.assigment(statement)
                continue
            if statement["type"] == "read":

                continue
            if statement["type"] == "read":

                continue
            if statement["type"] == "read":

                continue


