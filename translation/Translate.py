from torchgen.executorch.api.et_cpp import arguments

from Errors_custom import ProcedureCreatedTwice, ProcedureDosntExist, VariableNotFoundError, \
    ProcedureCalledWithWrongAmoutOfArguments
from translation import Arytmetic, Systemic, Register, EndOfFileChanges, ValueLoader, LoopsAndIf


class Translator:

    def __init__(self, string_to_translate):
        self.text = string_to_translate
        #This dic has var_name : i, where i is indeks of this var in end code,
        #only execption is Variables["reg"] witch contains a var thats currently in register
        #and infor if it was changed thruout the program
        self.Variables = {}
        self.Variables["0_number_of_vars"] = 1
        self.Variables["0_reg"] = 0
        self.decripted = ""
        self.register = Register(self.Variables)
        self.arytmetic = Arytmetic(self.Variables, self.register)
        self.systemic = Systemic(self.Variables, self.register)
        self.value_loader = ValueLoader(self.Variables, self.register, self.arytmetic, self.systemic)
        self.loops_and_if = LoopsAndIf(self.Variables, self.register, self.arytmetic, self.systemic, self.value_loader)
        self.Variables_for_proc = {}
        self.no_of_vars = 1


    def translate(self):
        main = self.text["program"]
        procedures = self.text["procedures"]
        if procedures is None:
            print("NIE MA PROCEDUR")
        else:
            self.translate_procedures(procedures)
        self.translate_main(main)
        self.end_file_changes()

    def translate_main(self, main):
        self.declaration(main["declarations"])
        self.decripted += self.statements(main["statements"])


    def translate_procedures(self, procedures):
        whole_code = ""
        for proc in procedures:
            single_proc_code = self.translate_procedure(proc)
            whole_code += single_proc_code
        self.decripted += whole_code
        return whole_code
#{"type" : "procedure", "declarations" : p.declarations, "body": p.statements, "head" : p.proc_head, 'lineno':p.lineno}
#return {"type": "proc_head", "name" : p.IDENTIFIER, "args": p.args_decl, 'lineno':p.lineno}
    def translate_procedure(self, procedure):
        decla = procedure["declarations"]
        body= procedure["body"]
        args = procedure["head"]["args"]
        name = procedure["head"]["name"]

        comand, vars_for_proc, pointers = self.declaration_proceduer(decla, args)
        self.register.set_pointer_vars(pointers)
        self.Variables_for_proc[f"0_Proc_{name}"] = {"Variables" : vars_for_proc, "pointers": pointers}
        body_code = self.translate_body_of_procedure(name, body)
        code = comand + self.register.add_statick_mark(f"0_Proc_{name}") + body_code + "\n" #TODO: erase \n after ur done testing

        return code


    def translate_body_of_procedure(self, name, body):
        Vars_full_dic = self.Variables_for_proc[f"0_Proc_{name}"]
        org_vars = self.Variables.copy()
        self.register.set_Variables(Vars_full_dic["Variables"])
        self.register.set_pointer_vars(Vars_full_dic["pointers"])
        print(f"vars in tsanslate: {self.Variables}, orginal: {org_vars}, register: {self.register.Variables}")
        body_code = self.statements(body)
        self.Variables["0_number_of_vars"] = Vars_full_dic["Variables"]["0_number_of_vars"]
        self.no_of_vars = self.Variables["0_number_of_vars"]
        self.register.set_Variables(org_vars)
        self.register.clear_pointers()
        return body_code


    def declaration_proceduer(self, declarations, args):
        vars_for_proc = {}
        vars_for_proc["0_number_of_vars"] = self.Variables["0_number_of_vars"]
        comand = ""
        for var_element in declarations:
            if var_element["type"] == "variable":
                var = var_element["name"]
                vars_for_proc[var] = vars_for_proc["0_number_of_vars"]
                vars_for_proc["0_number_of_vars"] += 1
            # if var_element["type"] == "table": #TODO: guess
            #     table_name = var_element["name"]
            #     line_no = var_element["lineno"]
            #     start = var_element["range"]["start"]
            #     end = var_element["range"]["end"]
            #     comand += self.systemic.create_tab(table_name, start, end, line_no)
        vars_for_proc["0_reg"] = 0
        vars_for_proc["_helper"] = vars_for_proc["0_number_of_vars"]
        vars_for_proc["0_number_of_vars"] += 1

        pointers = []
        for var_element in args:
            print("petla do dodawania argumentow zostala odpalona")
            print(var_element)
            if var_element["type"] == "variable":
                var = var_element["name"]
                vars_for_proc[var] = vars_for_proc["0_number_of_vars"]
                vars_for_proc["0_number_of_vars"] += 1
                pointers.append(var)
        return comand, vars_for_proc, pointers



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
        self.Variables["0_number_of_vars"] = self.no_of_vars
        comand = ""
        for var_element in variabouls:
            if var_element["type"] == "variable":
                var = var_element["name"]
                self.Variables[var] = self.Variables["0_number_of_vars"]
                self.Variables["0_number_of_vars"] += 1
            if var_element["type"] == "table":
                table_name = var_element["name"]
                line_no = var_element["lineno"]
                start = var_element["range"]["start"]
                end = var_element["range"]["end"]
                comand += self.systemic.create_tab(table_name, start, end, line_no)
        self.Variables["0_reg"] = 0
        self.Variables["_helper"] = self.Variables["0_number_of_vars"]
        self.Variables["0_number_of_vars"] += 1
        self.decripted += comand


    def statements(self, statments_tab):
        print("Starting statements")
        print(statments_tab)

        code = ""
        for statement in statments_tab:
            print(statement)
            self.register.lineno = statement["lineno"]
            line = ""
            if statement["type"] == "if":
                body = self.statements(statement["body"])
                if statement["else"] is not None:
                    else_body = self.statements(statement["else"])
                else:
                    else_body = None
                line += self.loops_and_if.if_statement(statement, body, else_body)

            if statement["type"] == "loop":
                body = self.statements(statement["body"])
                line = self.loops_and_if.loop_statement(statement, body, statement)
            if statement["type"] == "read":
                line = self.systemic.read(statement)
            if statement["type"] == "write":
                exp = self.value_loader.save_value_from_statement_in_reg(statement["value"])
                line = exp + self.systemic.write_var("reg")
            if statement["type"] == "assignment":
                if statement["variable_type"] == "variable":
                    exp = self.value_loader.save_value_from_statement_in_reg(statement["value"])
                    asign_to = self.systemic.assigment_reg(statement["variable"]["name"])
                    line = exp + asign_to
                if statement["variable_type"] == "table":
                    line = self.value_loader.save_value_from_statement_in_reg(statement["indeks"]) #reg = i
                    line_h, helper = self.systemic.store_tab_addres_in__helper(statement["variable"])
                    line +=  line_h #_helper = faktyczne i (adres tab[i] w vm)
                    line += self.value_loader.save_value_from_statement_in_reg(statement["value"]) #reg = value po prawej od znaku :=
                    line += self.register.store_i_var(helper) #adres który jest pod _helper (czyli adres tab[i]) = reg


            code += line


        return code
        