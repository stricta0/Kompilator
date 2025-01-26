from Errors_custom import VariableNotFoundError


class Register:
    def __init__(self, Variables):
        self.has_changed_since_load = False
        self.last_loaded_var_no = None
        self.Variables = Variables
        self.lineno = 0
        self.bool_exists = False
        self.zero_element = None
        self.one_element = None
        self.mark_zone = 0
        self.new_value_ind = 2
        self.pointer_vars = []


    def set_Variables(self, Variabels):
        self.Variables.clear()
        print(f"Variables got by set_variables: {Variabels}" )
        for key in Variabels:
            self.Variables[key] = Variabels[key]

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


    def load_var(self, var):

        self.check_if_variable_exists(var)
        if not self.has_changed_since_load and self.last_loaded_var_no == self.Variables[var]:
            return "" #already loaded
        else:
            self.has_changed_since_load = False
            self.last_loaded_var_no = self.Variables[var]
            if self.check_if_pointer(var):
                return f"LOADI {self.Variables[var]}\n"
            return f"LOAD {self.Variables[var]}\n"

    def store(self, var):
        print("SOME COMMMAND 10")
        self.check_if_variable_exists(var)
        self.has_changed_since_load = True #Somthing else changed the value
        if self.check_if_pointer(var):
            return f"STOREI {self.Variables[var]}\n"
        return f"STORE {self.Variables[var]}\n"


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
        print("SOME COMMMAND 9")
        self.check_if_variable_exists(var)
        self.has_changed_since_load = True
        if self.check_if_pointer(var):
            return f"ADDI {self.Variables[var]}\n"
        return f"ADD {self.Variables[var]}\n"

    def sub_var(self, var):
        print("SOME COMMMAND 7")
        self.check_if_variable_exists(var)
        self.has_changed_since_load = True
        if self.check_if_pointer(var):
            return f"SUBI {self.Variables[var]}\n"
        return f"SUB {self.Variables[var]}\n"

    def set_comand(self, x):
        print("SOME COMMMAND 5")
        self.has_changed_since_load = True
        return f"SET {x}\n"

    def put_var(self, var_name):
        self.check_if_variable_exists(var_name)
        if self.check_if_pointer(var_name):
            return f"LOADI {self.Variables[var_name]}\nPUT {self.Variables["0_reg"]}"
        return f"PUT {self.Variables[var_name]}\n"

    def get_comand(self, i):
        self.check_if_variable_exists(i)
        self.has_changed_since_load = True
        if self.check_if_pointer(i):
            return f"GET {self.Variables["0_reg"]}\nSTOREI {self.Variables[i]}"
        return f"GET {self.Variables[i]}\n"


    def make_0_and_1_if_dont_exist_already(self):
        if self.bool_exists:
            return ""
        self.bool_exists = True
        comand = ""
        comand += self.set_comand(0)
        line, self.zero_element = self.store_helper_multiple_vars()
        comand += line
        comand += self.set_comand(1)
        line, self.one_element= self.store_helper_multiple_vars()
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

    def add_statick_mark(self, mark_name):
        return f"MARKER {mark_name}\n"

    def add_mark(self, mark_name):
        return f"MARKER {mark_name}_{self.mark_zone}\n"

    def new_marks(self):
        self.mark_zone += 1

    def load_i_var(self, val):
        self.check_if_variable_exists(val)
        self.has_changed_since_load = True
        return f"LOADI {self.Variables[val]}\n"


    def store_i_var(self, var_name):
        self.check_if_variable_exists(var_name)
        self.has_changed_since_load = True
        return f"STOREI {self.Variables[var_name]}\n"

    def create_var(self, var_name):
        self.Variables[var_name] = self.Variables['0_number_of_vars']
        self.Variables['0_number_of_vars'] += 1
        self.has_changed_since_load = True