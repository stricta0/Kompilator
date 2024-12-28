class FileMenadger:
    def read(self, file_name):
        try:
            with open(file_name, 'r') as f:
                file = f.read()
        except FileNotFoundError:
            print(f"Kompilation Error - file not found at: {file_name}")
            exit()
