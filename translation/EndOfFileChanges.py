class EndOfFileChanges:
    def __init__(self, comands):
        self.comand = comands

    def marks_adj(self):
        print("MARKS_ADJ IN PLAY")
        marks_dic = {}
        comands_list = self.comand.split("\n")
        for i in range(len(comands_list)):
            comand = comands_list[i]
            if comand[:6] == "MARKER":
                comand_l = comand.split(" ")
                mark_name = comand_l[1]
                marks_dic[mark_name] = i+1
        new_comand = ""
        for i in range(len(comands_list)):
            comand = comands_list[i]
            if comand[:6] == "MARKER":
                continue
            if comand[:6] == "MARKED":
                comand_l = comand.split(" ")
                if comand_l[2] not in marks_dic:
                    print(f"stworzyles marka: {comand_l[2]} ale nie znaleziono go w markerach: {marks_dic}")
                    return None
                comand = f"{comand_l[1]} {marks_dic[comand_l[2]] - (i+1)}"
            new_comand += comand + "\n"
        return new_comand
