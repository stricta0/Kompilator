import sys
import Gramar
from Gramar import CalcLexer, CalcParser, PrepareData, GF1234577

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
    lexer = CalcLexer()
    parser = CalcParser()
    data_tool = PrepareData()
    # Pobierz nazwę pliku od użytkownika
    liniki = data_tool.prep_data(file)
    print(liniki)
    data_tool.run_onp(liniki, lexer, parser)