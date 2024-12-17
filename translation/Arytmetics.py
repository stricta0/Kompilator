class Arytmetic:
    def __init__(self, Variables):
        self.Variables = Variables

    def assigment(self, statement,var, value):
        var = statement["variable"]
        value = statement["value"]

        self.Variables[0] = 4

