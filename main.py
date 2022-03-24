from random import choice
from menu import *
from termcolor import colored


def main():
    choice()

def choice():

    while True:
        PaperT()
        printMenu()
        user_in = input('\nplease enter a number on the list: ')

        if user_in == '1':
            user = stocks.choose_account()
        elif user_in == '2':
            price = stocks.view_stockP()
        elif user_in == '0':
            clear()
            break
        else:
            clear()
            txt = colored(user_in, 'red')
            print(f'enter a number on the list please not {txt}')

#checks to make sure name is main
if __name__ == "__main__":
    main()