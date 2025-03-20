class CustomError(Exception):
    pass

class CodeError(CustomError):
    def __init__(self, line, error_message):
        super().__init__(f"Error at line {line}, with error message: {error_message}")
        self.line = line
        self.error_message = error_message

class InterpreterError(CodeError):
    def __init__(self, line, error_message):
        super().__init__(line, f"Error during Interpretation (logic): {error_message}")

class ProcedureError(InterpreterError):
    def __init__(self, line, error_message, function_name):
        super().__init__(line, f"Error in function {function_name} with message: {error_message}")

class ProcedureNotFoundError(ProcedureError):
    def __init__(self, line, function_name):
        super().__init__(line, "Procedure not found in this scope", function_name)

class ProcedureCreatedMoreThanOnceError(ProcedureError):
    def __init__(self, line, function_name):
        super().__init__(line, f"Procedure created for the second time", function_name)

class ProcedureCratedAfterCall(ProcedureError):
    def __init__(self, line, function_name):
        super().__init__(line, f"This procedure was created after this call", function_name)


class WrongAmoutOfArguments(ProcedureError):
    def __init__(self, line, function_name, function_ammount, call_ammount):
        super().__init__(line, f"Function takes {function_ammount} arguments but {call_ammount} were given", function_name)


class WrongTypesOfArguments(ProcedureError):
    def __init__(self, line, function_name, def_argument_type, def_argument_name, call_argument_type, call_argument_name):
        super().__init__(line, f"Function defined with argument {def_argument_name} of type {def_argument_type}, however in call argument {call_argument_name} has type {call_argument_type}", function_name)


class DoubleDeclarationOfArguments(CodeError):
    def __init__(self, line, argument_name):
        super().__init__(line, f"Argument: {argument_name} declared more than once")

class LexerError(CodeError):
    def __init__(self, line, error_message):
        super().__init__(line, f"Error during syntax characters check: {error_message}")


class PerserError(CodeError):
    def __init__(self, line, error_message):
        super().__init__(line, f"Error during syntax logic check (Perser): {error_message}")

class VariableNotFoundError(InterpreterError):
    def __init__(self, line, error_message, var_name):
        super().__init__(line, f"Variable {var_name} dosnt exist!. More info: {error_message}")


class VariableNotInitialize(InterpreterError):
    def __init__(self, line, error_message, var_name):
        super().__init__(line, f"Variable {var_name} wasnt initialize yet. More info: {error_message}")


class IteratorError(CodeError):
    def __init__(self, line, error_message):
        super().__init__(line, f"Error in for loop - cant change value of iterator: {error_message}")


class WrongTypeError(CodeError):
    def __init__(self, line, var, type_var, def_type_var):
        super().__init__(line, f"Error in types, variable {var} is of type {def_type_var} not {type_var}")
