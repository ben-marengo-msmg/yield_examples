class MyFileWriter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_obj = open(file_name, 'w')

    def __enter__(self):
        return self.file_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()
        if isinstance(exc_val, ZeroDivisionError):
            print(f'that was silly: {exc_val}')
            return True  # doesnt re-raise


with MyFileWriter('hello.txt') as f:
    f.write('foo')


with MyFileWriter('hello2.txt') as f:
    f.write('foo')
    print(1/0)

