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
        self.Variables["number_of_vars"] = 1
        comand = ""
        for var_element in variabouls:
            if var_element["type"] == "variable":
                var = var_element["name"]
                self.Variables[var] = self.Variables["number_of_vars"]
                self.Variables["number_of_vars"] += 1
            if var_element["type"] == "table":
                table_name = var_element["name"]
                line_no = var_element["lineno"]
                start = var_element["range"]["start"]
                end = var_element["range"]["end"]
                comand += self.systemic.create_tab(table_name, start, end, line_no)
        self.Variables["reg"] = 0
        self.Variables["_helper"] = self.Variables["number_of_vars"]
        self.Variables["number_of_vars"] += 1
        self.decripted += comand

    def save_value_from_statement_in_reg(self, statement): #save statment in reg

        if statement["type"] == "identifier":
            if statement["var_type"] == "var":
                return self.register.load_var(statement["name"])
            if statement["var_type"] == "table":
                comand = self.save_value_from_statement_in_reg(statement["indeks"])
                return comand + self.systemic.load_tab_i(statement['name'])
        if statement["type"] == "number":
            return self.register.set_comand(statement["value"])
        if statement["type"] == "expression":
            return self.arytmetic.solve_expression(statement)
        if statement["type"] == "comparison":
            return self.arytmetic.solve_comparison(statement)


    def statements(self, statments_tab):
        print("Starting statements")
        print(statments_tab)

        code = ""
        for statement in statments_tab:
            print(statement)
            self.register.lineno = statement["lineno"]
            line = ""
            if statement["type"] == "if":
                line = self.save_value_from_statement_in_reg(statement['check']) #load check into reg
                line += self.register.marked_jump("else_m", "JZERO")
                line += self.statements(statement["body"])
                line += self.register.marked_jump("end_m", "JUMP")
                line += self.register.add_mark("else_m")
                line += self.statements(statement["else"])
                line += self.register.add_mark("end_m")
                self.register.new_marks()

            if statement["type"] == "read":
                line = self.systemic.read(statement)
            if statement["type"] == "write":
                exp = self.save_value_from_statement_in_reg(statement["value"])
                line = exp + self.systemic.write_var("reg")
            if statement["type"] == "assignment":
                if statement["variable_type"] == "variable":
                    exp = self.save_value_from_statement_in_reg(statement["value"])
                    asign_to = self.systemic.assigment_reg(statement["variable"])
                    line = exp + asign_to
                if statement["variable_type"] == "table":
                    line = self.save_value_from_statement_in_reg(statement["indeks"]) #reg = i
                    line_h, helper = self.systemic.store_tab_addres_in__helper(statement["variable"])
                    line +=  line_h #_helper = faktyczne i (adres tab[i] w vm)
                    line += self.save_value_from_statement_in_reg(statement["value"]) #reg = value po prawej od znaku :=
                    line += self.register.store_i_var_number(helper) #adres który jest pod _helper (czyli adres tab[i]) = reg



            if statement["type"] == "read":
                pass

            if statement["type"] == "read":
                pass

            code += line

        self.decripted += code
        return code
        