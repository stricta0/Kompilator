from Errors_custom import WrongTypeError, VariableNotFoundError, WrongAmoutOfArguments, \
    ProcedureNotFoundError, ProcedureCratedAfterCall


class TypeChecker:
    def __init__(self, code):
        self.code = code
        self.Variables_with_type = {}
        self.declared_in_procedures = {}
        self.arguments_in_procedure = {}
        self.function_definiotons_places = {}
        self.line_no = 0

    def print_check(self):
        for el in self.declared_in_procedures:
            print(f"{'-' * 50}\n{el}:\ndeclared:\n{self.declared_in_procedures[el]}\narguments:\n{self.arguments_in_procedure[el]}\n{'-' * 50}\n")
    def check(self):
        self.declarations_and_arguments()
        #self.print_check()
        self.check_all_statements()

    def declarations_and_arguments(self):
        if self.code['procedures'] is not None:
            for proc in self.code['procedures']:
                declaration = proc["declarations"]
                args = proc["head"]["args"]
                name = proc["head"]["name"]
                self.procedures_arguemt_types(args, name)
                self.procedure_declarations_type(declaration, name)
                self.function_definiotons_places[name] = proc['head']["lineno"]
        name = "0_main"
        program = self.code["program"]
        dec = program["declarations"]
        self.procedure_declarations_type(dec, name)
        self.procedures_arguemt_types([], name)
        self.function_definiotons_places[name] = program["lineno"]

    def procedures_arguemt_types(self, args, name):
        self.arguments_in_procedure[name] = []
        for arg in args:
            self.arguments_in_procedure[name].append([arg["name"], arg["type"]])

    def procedure_declarations_type(self, declaration, name):
        self.declared_in_procedures[name] = []
        for dec in declaration:
            self.declared_in_procedures[name].append([dec["name"], dec["type"]])

    def check_all_statements(self):
        if self.code['procedures'] is not None:
            for proc in self.code['procedures']:
                name = proc["head"]["name"]
                statements = proc["body"]
                self.check_proc_statements(statements, name)
        name = "0_main"
        program = self.code["program"]
        statements = program["statements"]
        self.check_proc_statements(statements, name)
    def check_proc_statements(self, statements, function_name):
        for statement in statements:
            self.line_no = statement["lineno"]
            if statement["type"] == "if":
                self.check_proc_statements(statement["body"], function_name)
                if statement["else"] is not None:
                    self.check_proc_statements(statement["else"], function_name)
                self.check_comparison(statement['check'], function_name)

            if statement["type"] == "loop":
                if statement["loop_type"] == "for":
                    start = statement['start']
                    end = statement['end']
                    if start['type'] == "identifier":
                        self.check_identifier(start, function_name)
                    if end['type'] == "identifier":
                        self.check_identifier(end, function_name)
                else:
                    self.check_comparison(statement["check"], function_name)
                self.check_proc_statements(statement["body"], function_name)
            if statement["type"] == "assignment":
                self.check_singluar_var(statement["variable"]["name"], function_name, statement["variable_type"])
                self.check_expresion(statement['value'], function_name)
            if statement["type"] == "proc_call":
                self.check_if_you_can_call_this_function(function_name, statement["name"], statement["lineno"])
                self.check_proc_call(statement, function_name)
            if statement["type"] == "read":
                self.check_singluar_var(statement["variable"]["name"],function_name, statement["variable"]["type"])
            if statement["type"] == "write":
                self.check_expresion(statement["value"], function_name)

    def check_proc_call(self, statement, function_name):
        called_function_name = statement["name"]
        args_of_called = self.arguments_in_procedure[called_function_name]
        args_in_call = statement["args"]
        if len(args_of_called) != len(args_in_call):
            raise WrongAmoutOfArguments(self.line_no, called_function_name, len(args_of_called), len(args_in_call))
        for i in range(len(args_of_called)):
            local_arg_name = args_in_call[i]["name"]
            local_arg_type = self.find_type(local_arg_name, function_name)
            function_arg_name = args_of_called[i][0]
            function_arg_type = args_of_called[i][1]
            self.check_if_the_same_type(local_arg_name, local_arg_type, function_arg_type)

    def find_type(self, var, function_name):
        name_range_args = self.arguments_in_procedure[function_name]
        name_range_dec = self.declared_in_procedures[function_name]
        for i in range(len(name_range_dec)):
            var_name_dec = name_range_dec[i][0]
            var_type_dec = name_range_dec[i][1]
            if var_name_dec == var:
                return  var_type_dec
        for i in range(len(name_range_args)):
            var_name_dec = name_range_args[i][0]
            var_type_dec = name_range_args[i][1]
            if var_name_dec == var:
                return var_type_dec

        raise VariableNotFoundError(self.line_no, "", var)

    def check_comparison(self, comparison, function_name):
        self.check_expresion(comparison["left"], function_name)
        self.check_expresion(comparison["right"], function_name)
    def check_expresion(self, expresion, function_name):
        if expresion["type"] != "expression":
            if expresion["type"] == "identifier":
                self.check_identifier(expresion, function_name)
            return
        if expresion["left"] == "expression":
            self.check_expresion(expresion["left"], function_name)
        if expresion["right"] == "expression":
            self.check_expresion(expresion["right"], function_name)

        if expresion["left"] == "identifier":
            self.check_identifier(expresion["left"], function_name)
        if expresion["right"] == "identifier":
            self.check_identifier(expresion["right"], function_name)

    def check_identifier(self, indifire, function_name):
        self.check_singluar_var(indifire["name"], function_name, indifire["var_type"])
    def check_singluar_var(self, var, function_name, var_type):
        name_range_args = self.arguments_in_procedure[function_name]
        name_range_dec = self.declared_in_procedures[function_name]
        for i in range(len(name_range_dec)):
            var_name_dec = name_range_dec[i][0]
            var_type_dec = name_range_dec[i][1]
            if var_name_dec == var:
                self.check_if_the_same_type(var, var_type, var_type_dec)
                return
        for i in range(len(name_range_args)):
            var_name_dec = name_range_args[i][0]
            var_type_dec = name_range_args[i][1]
            if var_name_dec == var:
                self.check_if_the_same_type(var, var_type, var_type_dec)
                return

    def check_if_the_same_type(self, var, var_type, var_type_dec):
        if var_type == "variable":
            var_type = "var"
        if var_type_dec == "variable":
            var_type_dec = "var"
        if var_type != var_type_dec:
            raise WrongTypeError(self.line_no, var, var_type, var_type_dec)

    def check_if_you_can_call_this_function(self, function_name, called_function_name, lineno):
        if called_function_name not in self.function_definiotons_places:
            raise ProcedureNotFoundError(lineno, called_function_name)
        if self.function_definiotons_places[function_name] <= self.function_definiotons_places[called_function_name]:
            raise ProcedureCratedAfterCall(lineno, called_function_name)