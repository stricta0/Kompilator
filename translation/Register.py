from Errors_custom import VariableNotFoundError, VariableNotInitialize


class Register:
    def __init__(self, Variables, initialize_vars):
        self.mark_zone_half_static = 0
        self.initialize_vars = initialize_vars
        self.Variables = Variables
        self.lineno = 0
        self.zero_element = None
        self.one_element = None
        self.mark_zone = 0
        self.new_value_ind = 2
        self.pointer_vars = []
        self.GlobalVariables = {}

    def check_if_initialize(self, var, lineno):

        if var not in self.initialize_vars:
            raise VariableNotInitialize(lineno, "", var)
    def set_Variables(self, Variabels):
        self.Variables.clear()
        for key in Variabels:
            self.Variables[key] = Variabels[key]
        for key in self.GlobalVariables:
            self.Variables[key] = self.GlobalVariables[key]
    def add_to_pointers(self, pointers):
        self.pointer_vars += pointers

    def set_pointer_vars(self, pointers):
        self.pointer_vars = pointers.copy()

    def clear_pointers(self):
        self.pointer_vars.clear()

    def check_if_pointer(self, var):
        return var in self.pointer_vars

    def check_if_variable_exists(self, var):
        if var not in self.Variables:
            raise VariableNotFoundError(self.lineno, "Variable dosnt exists in this scope", var)


    def load_var(self, var, ignore_pointers=False):
        self.check_if_variable_exists(var)
        if self.check_if_pointer(var) and not ignore_pointers:
            return f"LOADI {self.Variables[var]}\n"
        return f"LOAD {self.Variables[var]}\n"

    def store(self, var, ignore_pointer=False):
        self.check_if_variable_exists(var)
        if self.check_if_pointer(var) and not ignore_pointer:
            return f"STOREI {self.Variables[var]}\n"
        return f"STORE {self.Variables[var]}\n"

    def store_indeks(self, indeks):
        return f"STORE {indeks}\n"


    def store_helper_multiple_vars(self):
        number_of_var = self.Variables['0_number_of_vars']
        self.Variables['0_number_of_vars'] += 1
        self.Variables[f"_{self.new_value_ind}"] = number_of_var
        self.new_value_ind += 1
        return f"STORE {number_of_var}\n", f"_{self.new_value_ind-1}"

    def create_var_but_dont_store(self):
        number_of_var = self.Variables['0_number_of_vars']
        self.Variables['0_number_of_vars'] += 1
        self.Variables[f"_{self.new_value_ind}"] = number_of_var
        self.new_value_ind += 1
        return f"_{self.new_value_ind-1}"

    def add_var(self, var):
        self.check_if_variable_exists(var)
        if self.check_if_pointer(var):
            return f"ADDI {self.Variables[var]}\n"
        return f"ADD {self.Variables[var]}\n"

    def sub_var(self, var):
        self.check_if_variable_exists(var)
        if self.check_if_pointer(var):
            return f"SUBI {self.Variables[var]}\n"
        return f"SUB {self.Variables[var]}\n"

    def set_comand(self, x):
        return f"SET {x}\n"

    def set_comand_mark_plus(self, x):
        return f"MSET {x}\n"

    def put_var(self, var_name):
        self.check_if_variable_exists(var_name)
        if self.check_if_pointer(var_name):
            return f"LOADI {self.Variables[var_name]}\nPUT {self.Variables['0_reg']}"
        return f"PUT {self.Variables[var_name]}\n"

    def get_comand(self, i):
        self.check_if_variable_exists(i)
        if self.check_if_pointer(i):
            return f"GET {self.Variables['0_reg']}\nSTOREI {self.Variables[i]}"
        return f"GET {self.Variables[i]}\n"


    def make_0_and_1(self):
        comand = ""
        comand += self.set_comand(0)
        line, self.zero_element = self.store_helper_multiple_vars()
        comand += line
        comand += self.set_comand(1)
        line, self.one_element= self.store_helper_multiple_vars()
        comand += line
        self.GlobalVariables[self.zero_element] = self.Variables[self.zero_element]
        self.GlobalVariables[self.one_element] = self.Variables[self.one_element]
        return comand

    def half(self):
        return "HALF\n"

    def jump(self, j):
        return f"JUMP {j}\n"

    def marked_jump(self, mark_name, jump_type):
        return f"MARKED {jump_type} {mark_name}_{self.mark_zone}\n"

    def static_marked_jump(self, mark_name, jump_type):
        return f"MARKED {jump_type} {mark_name}\n"

    def half_static_maked_jump(self, mark_name, jump_type):
        return f"MARKED {jump_type} {mark_name}_Hst{self.mark_zone_half_static}\n"

    def jpos(self, j):
        return f"JPOS {j}\n"

    def jzero(self, j):
        return f"JZERO {j}\n"

    def jneg(self, j):
        return f"JNEG {j}\n"

    def add_statick_mark(self, mark_name):
        return f"MARKER {mark_name}\n"

    def add_mark(self, mark_name):
        return f"MARKER {mark_name}_{self.mark_zone}\n"

    def add_half_static_mark(self, mark_name):
        return f"MARKER {mark_name}_Hst{self.mark_zone_half_static}\n"

    def incrament_half_static(self):
        self.mark_zone_half_static += 1

    def new_marks(self):
        self.mark_zone += 1

    def load_i_var(self, val):
        self.check_if_variable_exists(val)
        return f"LOADI {self.Variables[val]}\n"


    def store_i_var(self, var_name):
        self.check_if_variable_exists(var_name)
        return f"STOREI {self.Variables[var_name]}\n"

    def create_var(self, var_name):
        self.Variables[var_name] = self.Variables['0_number_of_vars']
        self.Variables['0_number_of_vars'] += 1

    def rtrn(self, var):
        return f"RTRN {self.Variables[var]}\n"

