from model.journal import Journal
from model.book import Book
from model.sol import Sol
from controller.mol_controller import MolController
from passlib.hash import sha256_crypt
import os, sys
import datetime

class SolController(MolController):

    def __init__(self, ui, reader, dao):
        self.ui = ui 
        self.reader = reader
        self.dao = dao
        self.start_sol()

    def start_sol(self):
        self.starter = True
        while self.starter:
            self.ui.pause()
            self.ui.clear()
            self.ui.print(self.ui.create_menu(self.ui.title0, self.ui.menu_sol))
            self.choice = self.ui.choose_option(self.ui.menu_sol)
            self.handle_menu()

    def handle_menu(self):
        if self.choice == 1:
            self.check_loan_status()
        elif self.choice == 2:
            self.check_loan_status_sol()
        elif self.choice == 3:
            self.check_current_loans_sol()
        elif self.choice == 4:
            self.return_item_sol()
        elif self.choice == 5:
            self.add_new()
        elif self.choice == 6:
            self.check_delayed_book()
        elif self.choice == 7:
            self.dao.save_library()
            self.dao.save_readers()
            self.starter = False
            return

#########################################
#for choice 2:
    def borrow_journal(self, journal):
        self.reader.borrowed_journals.append(journal) 
        self.ui.print(self.ui.title3a)
        self.ui.print(self.ui.title9 + str(self.return_date(journal)))

    def check_available_journal(self, journal):
        if not journal.is_borrowed:
            journal.is_borrowed = True
            return self.borrow_journal(journal) 
        self.ui.print(self.ui.title4a)
        self.ui.print(self.ui.title10)
        choice = self.ui.booking()
        self.book_book(choice, journal)

    def choose_journal_by_user(self):
        title, number = self.ui.journal_data_inputs()
        for journal in Journal.library_journals:
            if journal.title == title and journal.number == number:
                return self.check_available_journal(journal)
        return self.ui.print(self.ui.title2a)

    def check_loan_status_sol(self):
        if len(self.reader.borrowed_books) + len(self.reader.borrowed_journals) < 12:
            return self.choose_journal_by_user()
        self.ui.print(self.ui.title5)

    def book_book(self, choice, journal):
        if choice == '2':
            self.ui.print(self.ui.title12)
        elif choice == '1':
            time = 14
            if journal.is_short_term:
                time = 7
            end_date = journal.return_date + datetime.timedelta(days=time)
            journal.return_date = end_date
            self.reader.borrowed_journals.append(journal) 
            self.ui.print(self.ui.title12)
            journal.booked_book = self.ui.print(self.ui.title13 + str(journal.return_date - datetime.timedelta(days=time)) + '--->' + str(journal.return_date))
            
############################################################
#for choice 3:
    def check_current_loans_sol(self):
        if self.reader.borrowed_journals and self.reader.borrowed_books:
            books = [copy.id + ' ' + str(copy.return_date) for copy in self.reader.borrowed_books]
            journals = [journal.id + ' ' + str(journal.return_date) for journal in self.reader.borrowed_journals]
            self.all_positions = books + journals
            self.ui.print(self.ui.create_menu(self.ui.title6, self.all_positions))

        elif self.reader.borrowed_books:
            self.check_current_loans()
        elif self.reader.borrowed_journals:
            self.all_positions = [journal.id + ' ' + str(journal.return_date) for journal in self.reader.borrowed_journals]
            self.ui.print(self.ui.create_menu(self.ui.title6, self.all_positions))
        else:
            self.ui.print(self.ui.title8)

############################################################
#for choice 4:
    def return_item_sol(self):
        if not self.reader.borrowed_journals:
            self.return_item()
        else:
            borrowed_journals = [journal.id for journal in self.reader.borrowed_journals]
            borrowed_books = [copy.id for copy in self.reader.borrowed_books]
            borrowed = borrowed_journals + borrowed_books
            self.ui.print(self.ui.create_menu(self.ui.title6, borrowed))
            user = self.ui.choose_number_option(borrowed) - 1
            num, pos1, pos2 = borrowed[user].split('.')

            if '/' in pos2:
                for journal in Journal.library_journals:
                    if journal.id == borrowed[user]:
                        journal.is_borrowed = False
                        journal.return_date = None
                        for journal in self.reader.borrowed_journals:
                            if journal.id == borrowed[user]:
                                self.reader.borrowed_journals.remove(journal)       
            else:
                for book in Book.library_books:
                    if book.author == pos1 and book.title == pos2:
                        for copy in book.copies:
                            if copy.id == borrowed[user]:
                                copy.is_borrowed = False
                                # copy.return_date = None
                                for copy in self.reader.borrowed_books:
                                    if copy.id == borrowed[user]:
                                        self.reader.borrowed_books.remove(copy)                  
            self.ui.print(self.ui.title7)

#############################################################
#for choice 5:
    def add_new(self):
        kind = self.ui.choose_member_kind()
        name, surname, password = self.ui.login_inputs()
        password = sha256_crypt.encrypt(password)

        if kind == '1':
            stuff = Sol(name, surname, password)
        elif kind == '2':
            self.add_new_member(name, surname, password)

#############################################################
    def check_delayed_book(self):
        today = datetime.date.today()
        for book in Book.library_books:
            for copy in book.copies:
                if copy.is_borrowed: 
                   if (today - copy.return_date).days > 1:
                        self.ui.print(copy.id)
        for journal in Journal.library_journals:
            if journal.is_borrowed:
                if (today - journal.return_date).days > 1:
                    self.ui.print(journal.id)
            
#############################################################

