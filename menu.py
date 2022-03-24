from itertools import accumulate
import requests
import random
from main import *
import os
from termcolor import colored
import finnhub




def menu():

    menu = {
        1 : 'choose account',
        2 : 'view stock price',
        3 : 'view holdings',
        4 : 'load holdings',
        0 : 'Exit'
        } 
    return menu

def PaperT():
    print(
    '''
 _______  _______  _______  _______  ______      _______  ______    _______  ______   _______  ______   
|       ||   _   ||       ||       ||    _ |    |       ||    _ |  |   _   ||      | |       ||    _ |  
|    _  ||  |_|  ||    _  ||    ___||   | ||    |_     _||   | ||  |  |_|  ||  _    ||    ___||   | ||  
|   |_| ||       ||   |_| ||   |___ |   |_||_     |   |  |   |_||_ |       || | |   ||   |___ |   |_||_ 
|    ___||       ||    ___||    ___||    __  |    |   |  |    __  ||       || |_|   ||    ___||    __  |
|   |    |   _   ||   |    |   |___ |   |  | |    |   |  |   |  | ||   _   ||       ||   |___ |   |  | |
|___|    |__| |__||___|    |_______||___|  |_|    |___|  |___|  |_||__| |__||______| |_______||___|  |_|
    '''
    )

def printMenu():

    x = menu()

    for i in x:
        print(f'{i} {x[i]}')

def clear():
    """
    clears the terminal 
    """
    os.system('cls' if os.name=='nt' else 'clear')
    return("   ")

def choose_account():
    """
    chooses an account 
    isnt case senstive but does require y/n to start
    """
    print('\npress 0 to go back')
    Account = input('Do you have an account: Y/N: ')
    yesno = ['y', 'n']
    if str.lower(Account) in yesno:
        try:
            if str.lower(Account) == ('y'):
                Account = input('Enter your account name: ')
                txt = colored(f'Welcome {Account}', 'green')
                clear()
                print(txt)                
                return Account

            else:
                Account = input('Enter a name to create an account: ')
                txt = colored(f'Account created username: {Account}', 'green')
                clear()
                print(txt)
                return Account, 
        except:
            print('Not a valid account')
    elif Account == '0':
            clear()
        
    else:
        txt = colored(f'\nPlease enter Y or N not {Account}', 'red')
        print(txt)
        choose_account()

class stocks():

    def __init__(self, quit) -> None:
        self.yesno = quit

    def repeat(self, quit):
        pass

    def view_stockP():
        """
        does an api call to the finnhub api to get current stock price 
        {"c": 261.74,"h": 263.31,"l": 260.68,"o": 261.07,"pc": 259.45,"t": 1582641000}
        take the current price and return 
        """
        yesno = ['y', 'n']
        ticker = input('Enter stock ticker: ')
        ticker = ticker.upper()
        finnhub_client = finnhub.Client(api_key="c8tssuiad3i91cikglc0")
        data = (finnhub_client.quote(ticker))
        data = (data['c'])
        txt = f'\n{ticker} is ${data:.2f}'
        if data == 0:
            redtxt = colored(f'{ticker} is incorrect', 'red')
            print(f'Please enter a correct stock ticker {redtxt}')
            stocks.view_stockP()
        else:
            clear()
            print(txt)
            return data
        # keepgoing = input('do you want to search another: Y/N')
        # if str.lower(keepgoing) in yesno:
        #     stocks.view_stockP()
        # else:
        #     txt = colored(f'\nPlease enter Y or N not {keepgoing}', 'red')
        #     print(txt)
        #     choose_account()
        
    def holdings(self):
        pass

    def loadAccounts(self):
        pass

