from model.book_copy import Copy

class Book:

    library_books = []

    def __init__(self, author, title):
        self.title = title
        self.author = author
        self.copies = []

        Book.library_books.append(self)
        
    def add_copy(self, amount):
        self.copies.extend(Copy('.' + self.author + '.' + self.title)for i in range(amount))

    def __str__(self):
        free = 0
        for copy in self.copies:
            if not copy.is_borrowed:
                free += 1
        out = "\nauthor:{} title:{} available:{}\n".format(self.author, self.title, free)
        return out

