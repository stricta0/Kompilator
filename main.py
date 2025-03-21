import sys
import Gramar
from Errors_custom import CustomError
from Gramar import CalcLexer, CalcParser
from translation import Translator
from File_menadger import FileMenadger

file_menadger = FileMenadger()

#Fast is just for develompment
def bash_config(fast=False):
    #Open arguments - works only on windows OS
    if fast:
        file_name = ".\\test.txt"
        end_file_name = ".\\end.txt"
        file = file_menadger.read(file_name)
        return file, end_file_name
    if len(sys.argv) < 3:
        print("USAGE: py main.py 'code_to_compile.txt' 'name_of_compiled_file.txt'")
        sys.exit(1)
    file_name = sys.argv[1]
    end_file_name = sys.argv[2]

    #Check if code file exists
    try:
        file = file_menadger.read(file_name)
    except FileNotFoundError as e:
        print("Wrong arguments during bash config: ", e)
        exit()

    #Check if name for end file is allready taken
    while file_menadger.check_if_exists(end_file_name):
        rewrite_file = input("File of that name already exists, do you want to override it? (yes/no)")
        if rewrite_file == "no":
            end_file_name = input("Provide new file name: ")
        elif rewrite_file == "yes":
            break
        else:
            print("please write 'yes' to overide or 'no' to pick other name")

    # returns names of both files
    return file, end_file_name


# Główna funkcja
if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    file, end_file_name = bash_config()

    try:
        result = parser.parse(lexer.tokenize(file))
        transletor = Translator(result)
        transletor.translate()
        #transletor.print()
        res = transletor.get_code()
        file_menadger.write(end_file_name, res)
        print("\nSUCCES\n")
    except CustomError as e:
        print("Error during compilation")
        print(e)
    except FileNotFoundError as e:
        print("Error while dealing with file: ", e)