from Errors_custom import VariableNotFoundError, ProcedureNotFoundError, WrongAmoutOfArguments, \
    ProcedureCreatedMoreThanOnceError, DoubleDeclarationOfArguments
from translation import Arytmetic, Systemic, Register, EndOfFileChanges, ValueLoader, LoopsAndIf, TypeChecker


class Translator:

    def __init__(self, string_to_translate):
        self.text = string_to_translate
        self.Variables = {}
        self.Variables["0_number_of_vars"] = 1
        self.Variables["0_reg"] = 0
        self.decripted = ""
        self.initialize_vars = []
        self.register = Register(self.Variables, self.initialize_vars)
        self.systemic = Systemic(self.Variables, self.register)
        self.arytmetic = Arytmetic(self.Variables, self.register, self.systemic)
        self.value_loader = ValueLoader(self.Variables, self.register, self.arytmetic, self.systemic)
        self.loops_and_if = LoopsAndIf(self.Variables, self.register, self.arytmetic, self.systemic, self.value_loader)
        self.Variables_for_proc = {}



    def translate(self):
        checker = TypeChecker(self.text)
        checker.check()
        main = self.text["program"]
        procedures = self.text["procedures"]
        self.decripted += self.register.make_0_and_1()
        self.decripted += self.register.static_marked_jump("0_MAIN", "JUMP")
        if procedures is not None:
            self.translate_procedures(procedures)
        self.decripted += self.register.add_statick_mark("0_MAIN")
        self.translate_main(main)
        self.decripted += "HALT\n"
        self.end_file_changes()

    def translate_main(self, main):
        self.check_if_declaration_is_correct(main)
        self.declaration(main["declarations"])
        self.decripted += self.statements(main["statements"])


    def translate_procedures(self, procedures):
        whole_code = ""
        for proc in procedures:
            single_proc_code = self.translate_procedure(proc)
            self.decripted += single_proc_code
            whole_code += single_proc_code
        return whole_code
    def translate_procedure(self, procedure):
        self.check_if_function_declaration_is_correct(procedure)
        decla = procedure["declarations"]
        body= procedure["body"]
        args = procedure["head"]["args"]
        name = procedure["head"]["name"]

        comand, vars_for_proc, pointers, var_for_back_to_call = self.declaration_proceduer(decla, args)

        vars_for_proc[f"0_Proc_{name}_bcall"] = var_for_back_to_call
        self.register.GlobalVariables[f"0_Proc_{name}_bcall"] = var_for_back_to_call

        self.register.set_pointer_vars(pointers)

        self.Variables_for_proc[f"0_Proc_{name}"] = {"Variables" : vars_for_proc, "pointers": pointers, "var_for_back_to_call": var_for_back_to_call}
        body_code = self.translate_body_of_procedure(name, body)
        code = self.register.add_statick_mark(f"0_Proc_{name}") + comand + body_code
        self.register.Variables[f"0_Proc_{name}_bcall"] = var_for_back_to_call

        code += self.register.rtrn(f"0_Proc_{name}_bcall")
        return code

    def translate_body_of_procedure(self, name, body):
        Vars_full_dic = self.Variables_for_proc[f"0_Proc_{name}"]
        org_vars = self.Variables.copy()
        self.register.set_Variables(Vars_full_dic["Variables"])
        self.register.set_pointer_vars(Vars_full_dic["pointers"])
        body_code = self.statements(body)
        org_vars["0_number_of_vars"] = self.register.Variables["0_number_of_vars"]
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
            if var_element["type"] == "table":
                table_name = var_element["name"]
                line_no = var_element["lineno"]
                start = var_element["range"]["start"]
                end = var_element["range"]["end"]
                line_to_add, var_in_table_name = self.systemic.create_tab_in_procedure(table_name, start, end, line_no)
                ammount = end - start + 1
                vars_for_proc["0_number_of_vars"] += ammount
                comand += line_to_add
                vars_for_proc[table_name] = var_in_table_name

        vars_for_proc["0_reg"] = 0
        vars_for_proc["_helper"] = vars_for_proc["0_number_of_vars"]
        vars_for_proc["0_number_of_vars"] += 1
        var_containing_call_addres = vars_for_proc["0_number_of_vars"]
        vars_for_proc["0_number_of_vars"] += 1


        pointers = []
        for var_element in args:
            var = var_element["name"]
            vars_for_proc[var] = vars_for_proc["0_number_of_vars"]
            vars_for_proc["0_number_of_vars"] += 1
            pointers.append(var)
            self.initialize_vars.append(var)
        self.Variables["0_number_of_vars"] = vars_for_proc["0_number_of_vars"] + 1

        return comand, vars_for_proc, pointers, var_containing_call_addres

    def proc_call(self, statement, aditional_code):
        self.check_if_function_call_is_correct(statement)
        code = ""
        name = statement["name"]
        args = statement["args"]

        function_def_args = self.Variables_for_proc[f"0_Proc_{name}"]["pointers"] #names

        for i in range(len(args)):
            arg_in_call = args[i]
            name_of_arg_in_call = arg_in_call["name"]
            name_of_arg_in_def = function_def_args[i]
            code += self.set_pair_of_vars_in_procedure_call_and_def(name_of_arg_in_call, name_of_arg_in_def, name)

        code += self.register.set_comand_mark_plus(3)
        code += self.register.store(f"0_Proc_{name}_bcall")
        code += self.register.static_marked_jump(f"0_Proc_{name}", "JUMP")
        return code

    def set_pair_of_vars_in_procedure_call_and_def(self, name_of_arg_in_call, name_of_arg_in_def, function_name):
        code = ""
        if name_of_arg_in_call not in self.register.pointer_vars:
            code += self.register.set_comand(self.Variables[name_of_arg_in_call])
            code += self.register.store_indeks(self.Variables_for_proc[f"0_Proc_{function_name}"]["Variables"][name_of_arg_in_def])
        else:
            code += self.register.load_var(name_of_arg_in_call, True)
            code += self.register.store_indeks(
                self.Variables_for_proc[f"0_Proc_{function_name}"]["Variables"][name_of_arg_in_def])

        return code

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

    def declaration(self, variabouls):
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
        code = ""
        for statement in statments_tab:

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
                if statement["loop_type"] == "for":
                    iterator = statement["iterator"]
                    self.register.initialize_vars.append(iterator) #add iterator to initialazie values
                    self.register.create_var(iterator)
                body = self.statements(statement["body"])
                line += self.loops_and_if.loop_statement(statement, body, statement)
            if statement["type"] == "read":
                self.initialize_vars.append(statement["variable"]["name"])
                if statement["variable"]["type"] == "table":
                    line = self.register.set_comand(statement["variable"]["indeks"])  # reg = i
                    line_h, helper = self.systemic.store_tab_addres_in__helper(statement["variable"]["name"])
                    line += line_h  # _helper = faktyczne i (adres tab[i] w vm)
                    line += self.register.get_comand("0_reg")# reg = value po prawej od znaku :=
                    line += self.register.store_i_var(helper)
                else:
                    line = self.systemic.read(statement)
            if statement["type"] == "write":
                exp = self.value_loader.save_value_from_statement_in_reg(statement["value"])
                line = exp + self.systemic.write_var("0_reg")
            if statement["type"] == "assignment":
                if statement["variable_type"] == "variable":
                    exp = self.value_loader.save_value_from_statement_in_reg(statement["value"])
                    asign_to = self.systemic.assigment_reg(statement["variable"]["name"])
                    line = exp + asign_to
                if statement["variable_type"] == "table":
                    line = self.value_loader.save_value_from_statement_in_reg(statement["indeks"]) #reg = i
                    line_h, helper = self.systemic.store_tab_addres_in__helper(statement["variable"]["name"])
                    line += line_h #_helper = faktyczne i (adres tab[i] w vm)
                    line += self.value_loader.save_value_from_statement_in_reg(statement["value"]) #reg = value po prawej od znaku :=
                    line += self.register.store_i_var(helper) #adres który jest pod _helper (czyli adres tab[i]) = reg
                self.initialize_vars.append(statement["variable"]["name"])
            if statement["type"] == "proc_call":
                line = self.proc_call(statement, code)

            code += line

        return code

    def check_if_function_call_is_correct(self, call_statement):
        name = call_statement["name"]
        line_no = call_statement["lineno"]
        args = call_statement["args"]
        if f"0_Proc_{name}" not in self.Variables_for_proc:
            raise ProcedureNotFoundError(line_no, name)
        function_def_args = self.Variables_for_proc[f"0_Proc_{name}"]["pointers"]  # names
        if len(args) != len(function_def_args):  # i dont know
            raise WrongAmoutOfArguments(line_no, name, len(function_def_args), len(args))
        for arg in args:
            self.register.initialize_vars.append(arg["name"])

    def check_if_function_declaration_is_correct(self, procedure):
        decla = procedure["declarations"]
        args = procedure["head"]["args"]
        name = procedure["head"]["name"]
        line = procedure["lineno"]

        if f"0_Proc_{name}" in self.Variables_for_proc:
            raise ProcedureCreatedMoreThanOnceError(line, name)

        names = []
        for arg in args:
            n = arg["name"]
            if n in names:
                raise DoubleDeclarationOfArguments(line, n)
            names.append(n)
        for arg in decla:
            n = arg["name"]
            if n in names:
                raise DoubleDeclarationOfArguments(line, n)
            names.append(n)

    def check_if_declaration_is_correct(self, main):
        decla = main["declarations"]
        line = main["lineno"]
        names = []
        for arg in decla:
            n = arg["name"]
            if n in names:
                raise DoubleDeclarationOfArguments(line, n)
            names.append(n)

