class EndOfFileChanges:
    def __init__(self, comands):
        self.comand = comands
    def test_print(self, new_comands, marks_dic):
        for i in range(len(new_comands)):
            print(f"{i}: {new_comands[i]}")
        print(marks_dic)
    def test_print_no_marks(self):
        new_comands = self.comand.strip().split("\n")
        for i in range(len(new_comands)):
            print(f"{i}: {new_comands[i]}")
    def marks_adj(self):
        #self.test_print_no_marks()
        marks_dic = {}
        comands_list = self.comand.split("\n")
        line_counter = 0
        new_comands_list = []
        for i in range(len(comands_list)):
            comand = comands_list[i]
            if comand[:6] == "MARKER":
                comand_l = comand.split(" ")
                mark_name = comand_l[1]
                marks_dic[mark_name] = line_counter #was = i
            else:
                new_comands_list.append(comand)
                line_counter += 1

        new_comand = ""
        for i in range(len(new_comands_list)):
            comand = new_comands_list[i]
            if comand[:6] == "MARKED":
                comand_l = comand.split(" ")
                comand = f"{comand_l[1]} {marks_dic[comand_l[2]] - i}"
            if i != len(new_comands_list) - 1:
                new_comand += comand + "\n"
            else:
                new_comand += comand
        return self.set_marks_adj(new_comand)

    def set_marks_adj(self, comands):
        comands = comands.strip().split("\n")
        resoult = ""
        for i in range(len(comands)):
            com = comands[i]
            if com[:4] == "MSET":
                com = com.split(" ")
                new_com = f"SET {int(com[1]) + i}"
                resoult += new_com
            else:
                resoult += com
            if i != len(comands) - 1:
                resoult += "\n"
        return resoult


