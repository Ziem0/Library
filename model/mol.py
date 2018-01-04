class Mol:

    all_readers = []
    index = 1

    def __init__(self, name, surname, password):
        self.name = name
        self.surname = surname
        self.password = password
        self.email = self.name + '.' + self.surname + '@gmail.com'
        self.borrowed_books = []

        Mol.all_readers.append(self)
        Mol.index += 1
