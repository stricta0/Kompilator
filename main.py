import sys
import Gramar
from Gramar import CalcLexer, CalcParser
from translation import Translator

if len(sys.argv) < 2:
    print("Podaj przynajmniej jeden argument!")
    sys.exit(1)

file_name = sys.argv[1]

try:
    with open(file_name, 'r') as f:
        file = f.read()
except FileNotFoundError:
    print(f"Kompilation Error - file not found at: {file_name}")
    exit()



# Główna funkcja
if __name__ == '__main__':
    lexer = CalcLexer()        # Tworzymy instancję analizatora leksykalnego
    parser = CalcParser()      # Tworzymy instancję analizatora składniowego

    print("Tokens:")
    for tok in lexer.tokenize(file):
        print(tok)

    print("Lexing and parsing the file...")
    try:
        # Najpierw przepuszczamy plik przez lexer, potem parser
        result = parser.parse(lexer.tokenize(file))
        transletor = Translator(result)
        transletor.translate()
        transletor.print()
        transletor.statements()
        print(transletor.Variables)
        # print("Parsing completed successfully!")
        # print("Result: ", result)  # Wynik parsowania (zdefiniowany przez reguły)
        # print(result["declarations"])
    except Exception as e:
        print("Error during parsing: ", e)

