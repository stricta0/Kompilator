from translation import Arytmetic, Systemic

class Translator:

    def __init__(self, string_to_translate):
        self.text = string_to_translate
        self.Variables = {}
        self.decripted = ""

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

    def statements(self):
        arytmetic = Arytmetic(self.Variables)
        systemic = Systemic(self.Variables)
        for statement in self.text["statements"]:
            if statement["type"] == "read":
                systemic.read(statement)
                continue
            if statement["type"] == "assignment":
                arytmetic.assigment(statement, statement["variable"],statement["value"])
                continue
            if statement["type"] == "read":

                continue
            if statement["type"] == "read":

                continue
            if statement["type"] == "read":

                continue


