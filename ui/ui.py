import os
import getpass

class UI:

    menu = ['Browse', 'Login', 'New Member', 'Exit']
    title1 = 'Main Menu'
    title2 = 'Incorrect data!'
    title3 = 'Login as a library stuff'
    title4 = 'Correct!'

    @staticmethod
    def clear():
        os.system('clear')    

    @staticmethod
    def pause():
        out = input('Press ENTER to continue..')
        return out

    @staticmethod
    def searching_input():
        user = input('Search by first letter: ')
        return user

    @staticmethod
    def print(it):
        print(it)

    @staticmethod
    def create_menu(title, menu):
        out = '\n' + title + '\n\n'
        for n,option in enumerate(menu,1):
            out += '{}. {}\n'.format(n, option)
        return out 

    @staticmethod
    def choose_option(menu):
        user = 0
        while user < 1 or user > len(menu):
            try:
                user = int(input('choose option: '))
            except ValueError:
                print('Invalid value!')
        return user

    @staticmethod
    def book_data_inputs():
        author = input('author: ')
        title = input('title: ')
        return author, title 

    @staticmethod
    def journal_data_inputs():
        title = input('title: ')
        number = input('number: ')
        return title, number

    @staticmethod
    def choose_number_option(options):
        user = 0
        while user < 1 or user > len(options):
            try: 
                user = int(input('choose a number: '))
            except ValueError:
                print('Invalid value!')
        return user    

    @staticmethod
    def login_inputs():
        name = input('name: ')
        surname = input('surname: ')
        password = getpass.getpass('password: ')
        return name, surname, password

    @staticmethod
    def choose_member_kind():
        member = input('1 for STUFF, 2 for MEMBER: ')
        return member

    @staticmethod
    def booking():
        booking = input('1 for YES, 2 for NO: ')
        return booking