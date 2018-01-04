from controller.mol_controller import MolController
from controller.sol_controller import SolController
from model.mol import Mol
from model.book import Book
from model.journal import Journal
from passlib.hash import sha256_crypt
import getpass
import os, sys, time


class Controller:

    def __init__(self, ui, ui_readers, dao):
        self.ui = ui
        self.ui_readers = ui_readers
        self.dao = dao
        self.dao.load_library()
        self.dao.load_readers()
        self.start_controller()

    def start_controller(self):
        while 1:
            self.ui.clear()
            self.ui.print(self.ui.create_menu(self.ui.title1, self.ui.menu))
            self.choice = self.ui.choose_option(self.ui.menu)
            self.handle_menu()

    def handle_menu(self):
        if self.choice == 1:
            self.browse()
        elif self.choice == 2:
            self.log()
        elif self.choice == 3:
            self.add_new_person()
        elif self.choice == 4:
            sys.exit('See you later!')

##############################################################
#for choice 1:
    def browse(self):
        user = self.ui.searching_input()
        self.ui.clear()
        for book in Book.library_books:
            if book.author.startswith(user) or book.title.startswith(user):
                self.ui.print(book)
        for journal in Journal.library_journals:
            if journal.title.startswith(user) or journal.number.startswith(user):
                self.ui.print(journal)
        self.ui.pause()

##############################################################
#for choice 2:
    def log(self):
        name, surname, password = self.ui.login_inputs()
        for member in Mol.all_readers:
            if member.name == name and member.surname == surname:
                if sha256_crypt.verify(password, member.password):
                    time.sleep(1)
                    self.ui.print(self.ui.title4)
                    time.sleep(0.5)
                    return self.choose_controller(member)
        self.ui.print(self.ui.title2)
        return self.ui.pause()


    def choose_controller(self, member):
        if member.__class__.__name__ == 'Mol':
            MolController(self.ui_readers, member, self.dao)
        else:
            SolController(self.ui_readers, member, self.dao)

###############################################################
#for choice 3:
    def add_new_person(self):
        self.ui.print(self.ui.title3)
        self.log()
