class Copy:

    index = 1

    def __init__(self, initials):
        self.is_borrowed = False
        self.id = str(Copy.index) + initials
        self.is_short_term = False
        self.return_date = None

        Copy.index += 1

    
