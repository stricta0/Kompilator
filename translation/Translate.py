from translation import Arytmetic, Systemic, Register

class Translator:

    def __init__(self, string_to_translate):
        self.text = string_to_translate
        #This dic has var_name : i, where i is indeks of this var in end code,
        #only execption is Variables["reg"] witch contains a var thats currently in register
        #and infor if it was changed thruout the program
        self.Variables = {}
        self.Variables["first_empty"] = 1
        self.decripted = ""
        self.register = Register(self.Variables)

    def translate(self):
        self.declaration(self.text["declarations"])
        print("deklaracja")
        self.statements(self.text["statements"])
        print("statments")

    def get_code(self):
        return self.decripted


    def print(self):
        print("Input: ")
        print(self.text)
        print("\n\nOutput: ")
        print(self.decripted)

    #nie musimy tworzyć zmiennych w kodzie - wystarczy zapamiętać gdzie
    #jaka zmienna się znajduje a potem korzystać z tych "adresów"
    def declaration(self, variabouls):
        i = 1
        for var in variabouls:
            self.Variables[var] = i
            i += 1
        self.Variables["reg"] = 0
        self.Variables["first_empty"] = i



    def statements(self, statments_tab):
        arytmetic = Arytmetic(self.Variables, self.register)
        systemic = Systemic(self.Variables, self.register)
        code = ""
        print("declaration of arytmetic and systemic ended")
        for statement in statments_tab:
            print(statement)
            line = ""
            if statement["type"] == "read":
                line = systemic.read(statement)
            if statement["type"] == "write":
                print("write")
                if statement["value"]["type"] == "identifier":
                    line = systemic.write_var(statement["value"]["name"])
                if statement["value"]["type"] == "number":
                    line = systemic.write_number(statement)
                if statement["value"]["type"] == "expression":
                    exp = arytmetic.solve_expression(statement["value"])
                    line = exp + systemic.write_var("reg")


            if statement["type"] == "assignment":
                # line = arytmetic.assigment(statement)
                if statement["value"]["type"] == "identifier":
                    line = systemic.assigment_var(statement["variable"],statement["value"]["name"])
                if statement["value"]["type"] == "number":
                    line = systemic.assigment_number(statement["variable"],statement["value"]["value"])
                if statement["value"]["type"] == "expression":
                    exp = arytmetic.solve_expression(statement["value"])
                    line = exp + systemic.assigment_reg(statement["variable"])

            if statement["type"] == "read":
                pass

            if statement["type"] == "read":
                pass

            code += line

        self.decripted = code