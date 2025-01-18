from Errors_custom import VariableNotFoundError


class Register:
    def __init__(self, Variables):
        self.has_changed_since_load = False
        self.last_loaded_var_no = None
        self.Variables = Variables
        self.lineno = 0
        self.bool_exists = False
        self.zero_indeks = None
        self.one_indeks = None
        self.mark_zone = 0


    def check_if_variable_exists(self, var):
        if var not in self.Variables:
            raise VariableNotFoundError(self.lineno, "Variable dosnt exists in this scope", var)


    def load_var(self, var):
        self.check_if_variable_exists(var)
        if not self.has_changed_since_load and self.last_loaded_var_no == self.Variables[var]:
            return "" #already loaded
        else:
            self.has_changed_since_load = False
            self.last_loaded_var_no = self.Variables[var]
            return f"LOAD {self.Variables[var]}\n"

    def load_var_number(self, var_no):
        if not self.has_changed_since_load and self.last_loaded_var_no == var_no:
            return "" #already loaded
        else:
            self.has_changed_since_load = False
            self.last_loaded_var_no = var_no
            return f"LOAD {var_no}\n"

    def store(self, var):
        print("SOME COMMMAND 10")
        self.check_if_variable_exists(var)
        self.has_changed_since_load = True #Somthing else changed the value
        return f"STORE {self.Variables[var]}\n"

    def store_number_var(self, var):
        print("SOME COMMMAND 11")
        self.has_changed_since_load = True #Somthing else changed the value
        return f"STORE {var}\n"


    def store_helper_multiple_vars(self):
        number_of_var = self.Variables['number_of_vars']
        self.Variables['number_of_vars'] += 1
        return f"STORE {number_of_var}\n", number_of_var

    def create_var_but_dont_store(self):
        number_of_var = self.Variables['number_of_vars']
        self.Variables['number_of_vars'] += 1
        return number_of_var

    def add_var(self, var):
        print("SOME COMMMAND 9")
        self.check_if_variable_exists(var)
        self.has_changed_since_load = True
        return f"ADD {self.Variables[var]}\n"

    def add(self, var_no):
        print("SOME COMMMAND 8")
        self.has_changed_since_load = True
        return f"ADD {var_no}\n"

    def sub_var(self, var):
        print("SOME COMMMAND 7")
        self.check_if_variable_exists(var)
        self.has_changed_since_load = True
        return f"SUB {self.Variables[var]}\n"

    def sub(self, var_no):
        print("SOME COMMMAND 6")
        self.has_changed_since_load = True
        return f"SUB {var_no}\n"

    def set_comand(self, x):
        print("SOME COMMMAND 5")
        self.has_changed_since_load = True
        return f"SET {x}\n"

    def put(self, i):
        return f"PUT {i}\n"

    def put_var(self, var_name):
        self.check_if_variable_exists(var_name)
        return f"PUT {self.Variables[var_name]}\n"

    def get_comand(self, i):
        print("SOME COMMMAND 4")
        self.has_changed_since_load = True
        return f"GET {i}\n"

    def get_comand_var(self, var_name):
        print("SOME COMMMAND 3")
        self.check_if_variable_exists(var_name)
        self.has_changed_since_load = True
        return f"GET {self.Variables[var_name]}\n"

    def go_back_to_last_reg(self):
        self.has_changed_since_load = False
        return f"LOAD {self.last_loaded_var_no}\n"

    def make_0_and_1_if_dont_exist_already(self):
        if self.bool_exists:
            return ""
        self.bool_exists = True
        comand = ""
        comand += self.set_comand(0)
        line, self.zero_indeks = self.store_helper_multiple_vars()
        comand += line
        comand += self.set_comand(1)
        line, self.one_indeks = self.store_helper_multiple_vars()
        comand += line
        return comand

    def half(self):
        print("SOME COMMMAND 1")
        self.has_changed_since_load = True
        return "HALF\n"

    def jump(self, j):
        self.has_changed_since_load = True
        return f"JUMP {j}\n"

    def marked_jump(self, mark_name, jump_type):
        self.has_changed_since_load = True
        return f"MARKED {jump_type} {mark_name}_{self.mark_zone}\n"

    def jpos(self, j):
        self.has_changed_since_load = True
        return f"JPOS {j}\n"

    def jzero(self, j):
        self.has_changed_since_load = True
        return f"JZERO {j}\n"

    def jneg(self, j):
        self.has_changed_since_load = True
        return f"JNEG {j}\n"

    def add_mark(self, mark_name):
        return f"MARKER {mark_name}_{self.mark_zone}\n"

    def new_marks(self):
        self.mark_zone += 1

    def load_i_var_number(self, val):
        self.has_changed_since_load = True
        return f"LOADI {val}\n"

    def load_i_var(self, val):
        self.check_if_variable_exists(val)
        self.has_changed_since_load = True
        return f"LOADI {self.Variables[val]}\n"


    def store_i_var_number(self, val):
        self.has_changed_since_load = True
        return f"STOREI {val}\n"


    def store_i_var(self, var_name):
        self.check_if_variable_exists(var_name)
        self.has_changed_since_load = True
        return f"STOREI {self.Variables[var_name]}\n"