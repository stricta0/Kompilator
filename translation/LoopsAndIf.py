from translation import ValueLoader, Arytmetic, Systemic, Register, ArythmeticComparision
from Errors_custom import IteratorError
class LoopsAndIf:

    def __init__(self, Variables, register, arytmetic, systemic, value_loader):
        self.Variables = Variables
        self.register = register
        self.arytmetic = arytmetic
        self.systemic = systemic
        self.value_loader = value_loader

    def if_statement(self, statement, body, else_body):
        if statement["else"] is not None:
            line = self.value_loader.save_value_from_statement_in_reg(statement['check'])  # load check into reg
            line += self.register.marked_jump("else_m", "JZERO")
            line += body
            line += self.register.marked_jump("end_m", "JUMP")
            line += self.register.add_mark("else_m")
            line += else_body
            line += self.register.add_mark("end_m")
            self.register.new_marks()
        else:
            line = self.value_loader.save_value_from_statement_in_reg(statement['check'])
            line += self.register.marked_jump("end_m", "JZERO")
            line += body
            line += self.register.add_mark("end_m")
            self.register.new_marks()
        return line

    def loop_statement(self, statement, body, full_statement):
        if statement["loop_type"] == "for":
            self.look_for_iterator_change_in_body(full_statement)
            line = ""
            iterator = statement["iterator"]
            # self.register.create_var(iterator)
            line += self.value_loader.save_value_from_statement_in_reg(statement["start"])  #factorial(s,n);
            line += self.register.store(iterator) #iterator = start
            line += self.value_loader.save_value_from_statement_in_reg(statement["end"])
            line_l, i_end = self.register.store_helper_multiple_vars()
            line += line_l #i_end = end


            if statement["for_loop_type"] == "TO":
                #first, check if start<=end
                line += self.register.add_mark("LoopStart")
                line += self.arytmetic.custom_comparisone_of_vars(iterator, i_end, "<=") #comp
                line += self.register.marked_jump("LoopEnd", "JZERO")

                line += body

                line += self.register.load_var(iterator)
                line += self.register.add_var(self.register.one_element)
                line += self.register.store(iterator)
                #line += body

            if statement["for_loop_type"] == "DOWNTO":
                line += self.register.add_mark("LoopStart")
                line += self.arytmetic.custom_comparisone_of_vars(iterator, i_end, ">=")
                line += self.register.marked_jump("LoopEnd", "JZERO")

                line += body

                line += self.register.load_var(iterator)
                line += self.register.sub_var(self.register.one_element)
                line += self.register.store(iterator)

            #line += body
            line += self.register.marked_jump("LoopStart", "JUMP")
            line += self.register.add_mark("LoopEnd")
            self.register.new_marks()
            return line
        if statement["loop_type"] == "while":
            line = self.register.add_mark("LoopStart")
            #check
            line += self.arytmetic.solve_comparison(statement["check"])
            line += self.register.marked_jump("LoopEnd", "JZERO")
            line += body
            line += self.register.marked_jump("LoopStart", "JUMP")
            line += self.register.add_mark("LoopEnd")
            self.register.new_marks()
            return line
        if statement["loop_type"] == "repeat":
            line = self.register.add_mark("LoopStart")
            line += body
            line += self.arytmetic.solve_comparison(statement["check"])
            line += self.register.marked_jump("LoopEnd", "JPOS")
            line += self.register.marked_jump("LoopStart", "JUMP")
            line += self.register.add_mark("LoopEnd")
            self.register.new_marks()
            return line

    def look_for_iterator_change_in_body(self, full_statement):
        iterator = full_statement["iterator"]
        for statment in full_statement["body"]:

            if statment["type"] == "assignment":
                if statment['variable']['name'] == iterator:
                    raise IteratorError(statment["lineno"], f"Iterator changed on line: {statment['lineno']}\n")