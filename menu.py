from itertools import accumulate
from operator import contains
import string
from unittest import result
from xml.dom.minidom import Document

from numpy import choose
from main import *
from termcolor import colored
from pymongo import MongoClient
import finnhub, datetime, random, requests, os, pprint

def menu():

    menu = {
        1 : 'Choose Account',
        2 : 'View Stock Price',
        3 : 'Purchase',
        4 : 'View Holdings',
        5 : 'Load Holdings',
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

class stocks():

    def __init__() -> None:
        pass

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
                    with open('users.txt') as f:
                        if Account in f.read():
                            txt = colored(f'Welcome {Account}', 'green')
                            clear()
                            print(txt) 
                            f = open('user.txt',  'w')
                            f.write(Account)
                            f.close             
                            return Account
                        else:
                            print('Account not found please try again')
                            stocks.choose_account()

                else:
                    Account = input('Enter a name to create an account: ')
                    txt = colored(f'Account created username: {Account}', 'green')
                    clear()
                    print(txt)
                    newuser = open('users.txt', 'a')
                    newuser.writelines(Account)
                    newuser.close
                    user = open('user.txt', 'w')
                    user.write(f'\n{Account}')
                    user.close
                    return Account, 
            except:
                pass
        elif Account == '0':
                clear()
            
        else:
            txt = colored(f'\nPlease enter Y or N not {Account}', 'red')
            print(txt)
            stocks.choose_account()

    def addholdings(totalP, ticker, data, quant):
            """
            adds a stock purchase to the mongo db
            need to add read write to json
            reads current user from the user file
            """
            client = MongoClient() #connect to the server
            db = client.Stonks #returns an object pointing to db test 
            Pdate = datetime.datetime.now()
            with open('user.txt','r') as f:
                lines = f.readlines()
                user = lines[0]
                if lines == None:
                    stocks.choose_account()
            doc = {
                'User': user,
                'Ticker': ticker,
                'PricePer': data,
                '#Shares' : quant,
                'TotalPrice': f'{totalP:.2f}',
                'Date': Pdate
            }
            collection = db.Holdings
            doc_id = collection.insert_one(doc).inserted_id
            print(f'inserted {doc_id}')

    def view_stockP():
        """
        does an api call to the finnhub api to get current stock price 
        {"c": 261.74,"h": 263.31,"l": 260.68,"o": 261.07,"pc": 259.45,"t": 1582641000}
        take the current price and return 
        """
        ticker = input('Enter stock ticker: ')
        data = stocks.get_price(ticker)
        if data == 0:
            redtxt = colored(f'{ticker} is incorrect', 'red')
            print(f'Please enter a correct stock ticker {redtxt}')
            stocks.view_stockP()
        elif ticker == '0':
            clear()
            pass
        else:
            clear()
            print(f'\n{ticker} is ${data:.2f}')
            return data

    def get_price(ticker):
        ticker = ticker.upper()
        finnhub_client = finnhub.Client(api_key="c8tssuiad3i91cikglc0")
        data = (finnhub_client.quote(ticker))
        data = (data['c'])
        return data

    def purchase():
        """
        This function allows you to purchase a stock calls get_price for price 
        then asks user y/n to purchase 
        if yes then user is asked how many shares if shares is not a number it cancels the order
        if they to buy it calls mongoDB func and adds the purchase to the db 
        """
        yesno = ['y', 'n']
        ticker = input('Enter stock ticker: ')
        data = stocks.get_price(ticker)
        if data == 0:
            redtxt = colored(f'{ticker} is not a ticker', 'red')
            print(f'Please enter a correct stock ticker {redtxt}')
            stocks.purchase()
        else:  
            buy = input(f'\n{ticker} is ${data:.2f} would you like to buy y/n ')
            if str.lower(buy) in yesno:
                if str.lower(buy) == 'y':
                    txt = colored('WARNING', 'red')
                    print(f'{txt} if you dont enter a positive number your order will be canceled\n')
                    quant = input('How many shares do you want to buy: ')
                    try:
                        quant = float(quant)
                        quant = abs(quant)
                        totalP = float(quant) * data
                        clear()
                        stocks.addholdings(totalP, ticker, data, quant)
                        print(f'{quant} of {ticker} purchased for {totalP:.2f}')
                        return totalP
                    except:
                        clear()
                        txt = colored(f'{quant} is not a number order canceled', 'red')
                        print(f'{txt}')
                        pass   
                

    def holdings():
        with open('user.txt','r') as f:
            user = f.readlines()
            user = user[0]
            client = MongoClient() #connect to the server
            db = client.Stonks #returns an object pointing to db test
            clear()
            for holding in db.Holdings.find({'User': f'{user}'}):
                print('\n')
                pprint.pprint(f'{holding}')


    def loadAccounts():
        pass

