from pathlib import Path

class FileMenadger:
    def read(self, file_name):
        try:
            with open(file_name, 'r') as f:
                file = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Kompilation Error - file not found at: {file_name}")
        return file

    def check_if_exists(self, file_name):
        file_path = Path(file_name)
        if file_path.is_file():
            return True
        else:
            return False

    def write(self, file_name, text):
        try:
            with open(file_name, "w") as f:
                f.write(text)
        except OSError:
            raise FileNotFoundError(f"Something went wrong while creating txt file - please check your file_name ({file_name}) and OS settings")
