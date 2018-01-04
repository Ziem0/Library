class Journal:

    library_journals = []
    index = 1

    def __init__(self, title, number):
        self.title = title
        self.number = number
        self.id = str(Journal.index) + '.' + self.title + '.' + self.number
        self.is_borrowed = False
        self.is_short_term = False
        self.return_date = None


        Journal.library_journals.append(self)
        Journal.index += 1

    def __str__(self):
        available = 'NO'
        if not self.is_borrowed:
            available = 'YES'
        out = "\ntitle:{} year/month:{} available:{}\n".format(self.title, self.number, available)
        return out
