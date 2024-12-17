class PrepareData:
    def prep_data(self, plik):
        liniki = []
        plik = plik.strip()
        linika = ""
        continue_line = False
        comented = False
        is_operation = False
        for i in range(len(plik)):
            if plik[i] == "\n":
                if not continue_line:
                    if linika != "":
                        liniki.append(linika.strip())
                    linika = ""
                else:
                    continue_line = False
                comented = False
            elif plik[i] == "/":
                continue_line = True
            elif plik[i] == "#":
                comented = True
            else:
                if not comented:
                    linika += plik[i]
        if linika != "":
            liniki.append(linika.strip())
        return liniki

    def run_onp(self, liniki, lexer, parser):
        for line in liniki:
            print(f"Wyrażenie infiksowe: {line.strip()}")
            lexer_input = lexer.tokenize(line)
            parser.postfix = []  # Reset ONP dla nowej linii
            try:
                parser.parse(lexer_input)
            except Exception as e:
                print(f"Error raised while making onp, error mesage: {e}", end=", ")
                print("Skiping to next line")
                continue
            ##print("ONP:", ' '.join(parser.postfix))
