class Register:
    def __init__(self, Variables):
        self.has_changed_since_load = False
        self.last_loaded_var = None
        self.Variables = Variables

    def load_var(self, var):
        if not self.has_changed_since_load and self.last_loaded_var == var:
            return "" #already loaded
        else:
            self.has_changed_since_load = False
            self.last_loaded_var = var
            if var not in self.Variables:
                return "ERROR - Varible not defined in this scope\n"
            return f"LOAD {self.Variables[var]}\n"

    def store(self, var):
        if var not in self.Variables:
            return "ERROR - Varible not defined in this scope\n"
        self.has_changed_since_load = True #Somthing else changed the value
        return f"STORE {self.Variables[var]}\n"

    def store_helper(self):
        self.has_changed_since_load = True
        return f"STORE {self.Variables['first_empty']}\n"

    def add(self, var):
        if var not in self.Variables:
            return "ERROR - Varible not defined in this scope\n"
        self.has_changed_since_load = True
        return f"ADD {self.Variables[var]}\n"

    def sub(self, var):
        if var not in self.Variables:
            return "ERROR - Varible not defined in this scope\n"
        self.has_changed_since_load = True
        return f"SUB {self.Variables[var]}\n"

    def set_comand(self, x):
        self.has_changed_since_load = True
        return f"SET {x}\n"

    def put(self, i):
        return f"PUT {i}\n"

    def put_var(self, var_name):
        return f"PUT {self.Variables[var_name]}\n"

    def get_comand(self, i):
        self.has_changed_since_load = True
        return f"GET {i}\n"

    def get_comand_var(self, var_name):
        self.has_changed_since_load = True
        return f"GET {self.Variables[var_name]}\n"

