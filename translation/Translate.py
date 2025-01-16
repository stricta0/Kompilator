from translation import Arytmetic, Systemic, Register, EndOfFileChanges

class Translator:

    def __init__(self, string_to_translate):
        self.text = string_to_translate
        #This dic has var_name : i, where i is indeks of this var in end code,
        #only execption is Variables["reg"] witch contains a var thats currently in register
        #and infor if it was changed thruout the program
        self.Variables = {}
        self.Variables["number_of_vars"] = 1
        self.decripted = ""
        self.register = Register(self.Variables)
        self.arytmetic = Arytmetic(self.Variables, self.register)
        self.systemic = Systemic(self.Variables, self.register)


    def translate(self):
        self.declaration(self.text["declarations"])
        self.statements(self.text["statements"])
        self.end_file_changes()

    def end_file_changes(self):
        end_file = EndOfFileChanges(self.decripted)
        self.decripted = end_file.marks_adj()

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
        for var_element in variabouls:
            if var_element["type"] == "variable":
                var = var_element["name"]
                self.Variables[var] = i
                i += 1
            if var_element["type"] == "table":
                table_name = var_element["name"]
                line_no = var_element["lineno"]
                start = var_element["range"]["start"]
                end = var_element["range"]["end"]
                self.systemic.create_tab(table_name, start, end, line_no)
        self.Variables["reg"] = 0
        self.Variables["number_of_vars"] = i



    def statements(self, statments_tab):
        print("Starting statements")
        print(statments_tab)

        code = ""
        for statement in statments_tab:
            print(statement)
            self.register.lineno = statement["lineno"]
            line = ""
            if statement["type"] == "read":
                line = self.systemic.read(statement)
            if statement["type"] == "write":
                if statement["value"]["type"] == "identifier":
                    line = self.systemic.write_var(statement["value"]["name"])
                if statement["value"]["type"] == "number":
                    line = self.systemic.write_number(statement)
                if statement["value"]["type"] == "expression":
                    exp = self.arytmetic.solve_expression(statement["value"])
                    line = exp + self.systemic.write_var("reg")


            if statement["type"] == "assignment":
                # line = arytmetic.assigment(statement)
                if statement["value"]["type"] == "identifier":
                    line = self.systemic.assigment_var(statement["variable"],statement["value"]["name"])
                if statement["value"]["type"] == "number":
                    line = self.systemic.assigment_number(statement["variable"],statement["value"]["value"])
                if statement["value"]["type"] == "expression":
                    exp = self.arytmetic.solve_expression(statement["value"])
                    asign_to = self.systemic.assigment_reg(statement["variable"])
                    line = exp + asign_to
                    print("koniec exp")
                    print(f"exp: \n{exp}\nasign_to:\n{asign_to}")

            if statement["type"] == "read":
                pass

            if statement["type"] == "read":
                pass

            code += line

        self.decripted = code
        