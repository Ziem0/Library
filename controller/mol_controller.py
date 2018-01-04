import os, sys
import datetime
from model.mol import Mol
from model.book import Book

class MolController:

    def __init__(self, ui, reader, dao):
        self.ui = ui
        self.reader = reader
        self.dao = dao
        self.start_mol()

    def start_mol(self):
        self.starter = True
        while self.starter:
            self.ui.pause()
            self.ui.clear()
            self.ui.print(self.ui.create_menu(self.ui.title1, self.ui.menu))
            self.choice = self.ui.choose_option(self.ui.menu)
            self.handle_menu()
        
    def handle_menu(self):
        if self.choice == 1:
            self.check_loan_status()
        elif self.choice == 2:
            self.check_current_loans()
        elif self.choice == 3:
            self.return_item()
        elif self.choice == 4:
            self.dao.save_library()
            self.dao.save_readers()
            self.starter = False
            return
 
####################################################################
    #for choice 1:
    def borrow_book(self, copy):
        self.reader.borrowed_books.append(copy) 
        self.ui.print(self.ui.title3)
        self.ui.print(self.ui.title9 + str(self.return_date(copy)))

    def book_book(self, choice, copy):
        if choice == '2':
            self.ui.print(self.ui.title12)
        elif choice == '1':
            time = 14
            if copy.is_short_term:
                time = 7
            end_date = copy.return_date + datetime.timedelta(days=time)
            copy.return_date = end_date
            self.reader.borrowed_books.append(copy) 
            self.ui.print(self.ui.title12)
            copy.booked_book = self.ui.print(self.ui.title13 + str(copy.return_date - datetime.timedelta(days=time)) + '--->' + str(copy.return_date))

    def check_first_available_term(self, book):
        first_free = min(book.copies, key=lambda copy: copy.return_date)
        self.ui.print(self.ui.title11 + str(first_free.return_date))
        self.ui.print(self.ui.title10)
        choice = self.ui.booking()
        self.book_book(choice, first_free)

    def check_available_copy(self, book):
        for copy in book.copies:
            if not copy.is_borrowed:
                copy.is_borrowed = True
                return self.borrow_book(copy) 
        self.ui.print(self.ui.title4)
        self.check_first_available_term(book)

    def choose_book_by_user(self):
        author, title = self.ui.book_data_inputs()
        for book in Book.library_books:
            if book.author == author and book.title == title:
                return self.check_available_copy(book)
        return self.ui.print(self.ui.title2)

    def check_loan_status(self):
        if self.reader.__class__.__name__ == 'Mol':
            if len(self.reader.borrowed_books) < 6:
                return self.choose_book_by_user()
        else:
            if len(self.reader.borrowed_books) + len(self.reader.borrowed_journals) < 12:
                return self.choose_book_by_user()
        self.ui.print(self.ui.title5)
        
###################################################################
#for choice 2:
    def check_current_loans(self):
        menu = [copy.id + ' ' + str(copy.return_date) for copy in self.reader.borrowed_books]
        if menu:
            self.ui.print(self.ui.create_menu(self.ui.title6, menu))
        else:
            self.ui.print(self.ui.title8)

###################################################################
#for choice 3:
    def return_item(self):
        self.check_current_loans()
        user = self.ui.choose_number_option(self.reader.borrowed_books) - 1
        num, author, title = self.reader.borrowed_books[user].id.split('.')
        for book in Book.library_books:
            if book.author == author and book.title == title:
                for copy in book.copies:
                    if copy.id == self.reader.borrowed_books[user].id:
                        copy.is_borrowed = False 
                        copy.return_date = None
        del self.reader.borrowed_books[user]    
        self.ui.print(self.ui.title7)

###################################################################
    def add_new_member(self, name, surname, password):
        member = Mol(name, surname, password) 

###################################################################
    def return_date(self, item):
        time = 14
        if item.is_short_term:
            time = 7
        date_1 = datetime.date.today()
        end_date = date_1 + datetime.timedelta(days=time)
        item.return_date = end_date
        return item.return_date

####################################################################
