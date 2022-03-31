from random import choice
from menu import *
from termcolor import colored


def main():
    choice()

def choice():
    stocks.choose_account()

    while True:
        printMenu()
        user_in = input('\nplease enter a number on the list: ')

        if user_in == '1':
            user = stocks.choose_account()
        elif user_in == '2':
            price = stocks.view_stockP()
        elif user_in == '3':
            purchase = stocks.purchase()
        elif user_in == '4':
            pass
        elif user_in == '5':
            holdings = stocks.holdings()
        elif user_in == '6':
            Lholdings = stocks.loadHoldings()
        elif user_in == '7':
            Delholdings = stocks.remove()
        elif user_in == '8':
            Upholdings = stocks.updateH()
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