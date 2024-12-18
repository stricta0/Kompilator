class Systemic:
    def __init__(self, Variables, register):
        self.Variables = Variables
        self.register = register

    def read(self, statement):
        print("Change Var")
        var = statement["variable"]
        var_numebr = self.Variables[var]
        comad = f"GET {var_numebr}"
        return comad

    