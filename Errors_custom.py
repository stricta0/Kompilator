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


class LexerError(CodeError):
    def __init__(self, line, error_message):
        super().__init__(line, f"Error during syntax characters check: {error_message}")


class PerserError(CodeError):
    def __init__(self, line, error_message):
        super().__init__(line, f"Error during syntax logic check: {error_message}")

class VariableNotFoundError(InterpreterError):
    def __init__(self, line, error_message, var_name):
        super().__init__(line, f"Variable {var_name} dosnt exist!. More info: {error_message}")
