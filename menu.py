from itertools import accumulate
from main import *
from termcolor import colored
from pymongo import MongoClient
import finnhub, datetime, random, requests, os






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

    def __init__() -> None:
        pass
    def addholdings(totalP, ticker):
            """
            adds a stock purchase to the mongo db
            """
            client = MongoClient() #connect to the server
            db = client.Stonks #returns an object pointing to db test 
            Pdate = datetime.datetime.now()
            doc = {
                ticker: totalP,
                'date': Pdate
            }
            collection = db.temp
            doc_id = collection.insert_one(doc).inserted_id
            print(f'inserted {doc_id}')

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
        def Qshares(data, ticker):
                quant = input(f'How many shares of {ticker} do you want')
                try: 
                    quant = float(quant)
                    data = float(data)
                    if quant < 0:
                        print('The number must be positve')
                        Qshares(data, ticker)
                    else:
                        return quant
                except:
                    print('Please enter a number')
                    Qshares(data, ticker)
        if data == 0:
            redtxt = colored(f'{ticker} is incorrect', 'red')
            print(f'Please enter a correct stock ticker {redtxt}')
            stocks.view_stockP()
        else:
            clear()
            txt = f'\n{ticker} is ${data:.2f} would you like to buy y/n '
            buy = input(txt)
            if str.lower(buy) in yesno:
                if str.lower(buy) == 'y':
                    quant = Qshares(data, ticker)
                    totalP = data * quant
                    purchS = stocks.addholdings(totalP, ticker)
                    txt = f'{ticker} purchased for {data*quant:.2f}'
                    print(txt)
                else:
                    pass
            return data     

    def holdings():
        pass

    def loadAccounts():
        pass

