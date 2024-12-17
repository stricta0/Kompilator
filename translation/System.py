class Systemic:
    def __init__(self, Variables):
        self.Variables = Variables

    def read(self, statement):
        print("Change Var")
        self.Variables[0] = 123