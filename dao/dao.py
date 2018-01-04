from model.book import Book
from model.journal import Journal
from model.mol import Mol
from model.sol import Sol
import os, sys, csv
import datetime

class Dao:

    @staticmethod
    def load_library():
        if not os.path.isfile('static/books.csv'):
            raise FileNotFoundError
        else:
            with open('static/books.csv', 'r') as f:
                for item in f:
                    item = item.strip('\n')
                    item = item.split(',')
                    if item[0] == 'book':
                        author = item[1]
                        title = item[2]
                        book = Book(author, title)
                        book.add_copy(int(item[3]))
                        for copy in book.copies:
                            if item[5] == 'y':
                                copy.is_short_term = True
                        for copy in book.copies[:int(item[4])]:
                            copy.is_borrowed = True
                    else:
                        title = item[1]
                        number = item[2]
                        journal = Journal(title, number)
                        if item[3] == 'y':
                            journal.is_borrowed = True


    @staticmethod
    def save_library():
        with open('static/books.csv', 'w') as f:
            writer = csv.writer(f)
            for book in Book.library_books:
                borrowed = 0
                short_term = 'n'
                for copy in book.copies:
                    if copy.is_borrowed:
                        borrowed += 1 
                    elif copy.is_short_term:
                        short_term = 'y'
                writer.writerow(['book', book.author, book.title, len(book.copies), borrowed, short_term])
            for journal in Journal.library_journals:
                borrowed = 'n'
                if journal.is_borrowed:
                    borrowed = 'y'
                writer.writerow(['journal', journal.title, journal.number, borrowed])
                

    @staticmethod
    def load_readers():
        if not os.path.isfile('static/readers.csv'):
            raise FileNotFoundError
        else:
            with open('static/readers.csv', 'r') as f:
                for reader in f:
                    reader = reader.strip('\n')
                    reader = reader.split(',')
                    if reader[0] == 'staff':
                        person = Sol(reader[1], reader[2], reader[3])
                    elif reader[0] == 'member':
                        person = Mol(reader[1], reader[2], reader[3])
                    else:
                        if reader[0][-1].isdigit():
                            num, title, number = reader[0].split('.')
                            for journal in Journal.library_journals:
                                if journal.id == reader[0]:
                                    person.borrowed_journals.append(journal)
                                    if reader[1]:
                                        year, month, day = reader[1].split('-')
                                        journal.return_date = datetime.date(int(year), int(month), int(day))
                        else: 
                            num, author, title = reader[0].split('.')
                            for book in Book.library_books:
                                if book.author == author and book.title == title:
                                    for copy in book.copies:
                                        if copy.id == reader[0]:
                                            person.borrowed_books.append(copy)
                                            year, month, day = reader[1].split('-')
                                            copy.return_date = datetime.date(int(year), int(month), int(day))
                                            
    @staticmethod
    def save_readers():
        with open('static/readers.csv', 'w') as f:
            writer = csv.writer(f)
            for person in Mol.all_readers:
                if person.__class__.__name__ == 'Sol':
                    writer.writerow(['staff', person.name, person.surname, person.password])
                    for journal in person.borrowed_journals:
                        year, month, day = journal.return_date.year, journal.return_date.month, journal.return_date.day 
                        writer.writerow([journal.id, str(year) + '-' + str(month) + '-' + str(day)])
                elif person.__class__.__name__ == 'Mol':
                    writer.writerow(['member', person.name, person.surname, person.password])
                for copy in person.borrowed_books:
                    year, month, day = copy.return_date.year, copy.return_date.month, copy.return_date.day 
                    writer.writerow([copy.id, str(year) + '-' + str(month) + '-' + str(day)])
