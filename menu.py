import imp
from itertools import accumulate
from operator import contains
import string
from tokenize import group
from unittest import result
from xml.dom.minidom import Document
from collections import Counter as Count
import matplotlib.pyplot as plt
from numpy import choose
from main import *
from pymongo import *
from termcolor import colored
import finnhub, datetime, requests, os, json
import numpy as np
from bson.objectid import ObjectId
from alpha_vantage.timeseries import TimeSeries

def menu():
    """
    Stores users options in dictionay 
    """

    menu = {
        1 : 'Choose Account',
        2 : 'View Stock Price',
        3 : 'Purchase',
        4 : 'Sell',
        5 : 'View Holdings',
        6 : 'Load Holdings from JSON',
        7 : 'Delete Holdings',
        8 : 'Force Update Holdings',
        9 : 'Historical Prices Graph',
        0 : 'Exit'
        } 
    return menu

def PaperT():
    """
    ACII art 
    """
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
def clear():
    """
    clears the terminal 
    """
    os.system('cls' if os.name=='nt' else 'clear')
    return("   ")

def printMenu():
    """
    print s the menu so user can see the options
    """
    PaperT()
    x = menu()

    for i in x:
        print(f'{i} {x[i]}')



class stocks():

    def __init__() -> None:
        pass

    def choose_account():
        """
        chooses an account 
        isnt case senstive but does require y/n to start
        adds to a user document to store current user
        adds to users for reusability
        0 to exit
        """
        clear()
        print('Please log in')
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
                            name = colored(Account, 'red')
                            print(f'Account: {name} not found please try again')
                            stocks.choose_account()

                else:
                    Account = input('Enter a name to create an account: ')
                    txt = colored(f'Account created username: {Account}', 'green')
                    clear()
                    print(txt)
                    newuser = open('users.txt', 'a')
                    newuser.writelines(f'\n{Account}')
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
                'Ticker': ticker.upper(),
                'PricePer': f'{data:.2f}',
                '#Shares' : int(quant),
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
            print(f'\n{ticker.upper()} is ${data:.2f}')
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
        clear()
        yesno = ['y', 'n']
        ticker = input('Enter stock ticker: ')
        data = stocks.get_price(ticker)
        if data == 0:
            redtxt = colored(f'{ticker.upper()} is not a ticker', 'red')
            print(f'Please enter a correct stock ticker {redtxt}')
            stocks.purchase()
        else:  
            buy = input(f'\n{ticker.upper()} is ${data:.2f} would you like to buy y/n ')
            if str.lower(buy) in yesno:
                if str.lower(buy) == 'y':
                    txt = colored('WARNING', 'red')
                    print(f'{txt} if you dont enter a number your order will be canceled\n')
                    quant = input('How many shares do you want to buy: ')
                    try:
                        quant = float(quant)
                        quant = abs(quant)
                        totalP = float(quant) * data
                        clear()
                        stocks.addholdings(totalP, ticker, data, quant)
                        print(f'{int(quant)} shares of {ticker.upper()} purchased for {totalP:.2f}')
                        return totalP
                    except:
                        clear()
                        txt = colored(f'{quant} is not a number order canceled', 'red')
                        print(f'{txt}')
                        pass  

    def remove():
        client = MongoClient() #connect to the server
        db = client.Stonks #returns an object pointing to db test
        collection = db.Holdings
        clear()
        try:
            ticker = input('Enter stock ticker: ')
            ticker =  ticker.upper()
            T_del = {"Ticker": ticker}
            trash = collection.delete_many(T_del)
            print(f'{trash.deleted_count} documents deleted')
        except Exception as e:
            print("An exception occurred ::", e) 

    def sell(ticker):
        price = stocks.get_price(ticker)
             
    def holdings():
        """
        conects to db calls stonks collection
        finds holdings using the user 
        """
        clear()
        tickers = []
        try:
            with open('user.txt','r') as f:
                user = f.readlines()
                user = user[0]
                if user == None:
                    print('Please login')
                    pass
                else:
                    client = MongoClient() #connect to the server
                    db = client.Stonks #returns an object pointing to db test
                    clear()
                    print('=========================================')
                    for holding in db.Holdings.find({'User': f'{user}'}):
                        print('\n')
                        del holding['_id']
                        tickers.append(holding['Ticker'])
                        for key in holding:
                            print(f'{key}: {holding[key]}')
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            print('\nYour holdings contain:\n')
            count = Count(tickers)
            for key in count:
                print(f'{key}: {count[key]}', end=" ")
                        
    def loadHoldings():
        """
        Loads holdings from the data.json file
        checks if list to see if insert many is needed
        else just uses insert one
        """
        client = MongoClient() #connect to the server
        db = client.Stonks #returns an object pointing to db test
        collection = db.Holdings 
        clear()
        print('\n=========================================')
        try: 
            with open('data.json') as file:
                file_data = json.load(file)
            if isinstance(file_data, list):
                collection.insert_many(file_data)
                x = len(file_data)
                print(f'{x} docs inserted')
            else:
                collection.insert_one(file_data)
                print('1 file inserted')

        except Exception as e:
            print("An exception occurred ::", e)

    def updateH():
        """
        connects to mongo db
        prints all holdings in the db collection
        updates a single stock purchase to a different user based on _id
        """
        client = MongoClient() #connect to the server
        db = client.Stonks #returns an object pointing to db test
        collection = db.Holdings 
        clear()
        try:
            for holding in db.Holdings.find():
                print('\n')
                for key in holding:
                    print(f'{key}: {holding[key]}')
            update = input('please enter the _id you want to update: ')
            find = {'_id': ObjectId(update)}
            new_user = input('please enter the user you want to update: ')
            new = {"$set": {'User': new_user}}
            collection.update_one(find, new)
            changed = collection.find_one({'_id': ObjectId(update)})
            print('\n')
            clear()
            for key in changed:
                print(f'{key}: {changed[key]}')

        except Exception as e:
            print("An exception occurred ::", e)
        
    def sale(ticker):
        """
        deletes from the database after a sale
        """
        client = MongoClient() #connect to the server
        db = client.Stonks #returns an object pointing to db test
        collection = db.Holdings
        try:
            T_del = {"Ticker": ticker}
            trash = collection.delete_many(T_del)
            print(f'{trash.deleted_count} documents deleted')
        except Exception as e:
            print("An exception occurred ::", e) 

    def sell():
        """
        funtion to sell stocks
        """
        try:
            clear()
            avg = []
            num_shares = []
            ticker = input('Enter stock ticker: ')
            curr_price = stocks.get_price(ticker)
            client = MongoClient() #connect to the server
            db = client.Stonks #returns an object pointing to db test
            collection = db.Holdings 
            ticker = ticker.upper()
            with open('user.txt','r') as f:
                user = f.readlines()
                user = user[0]
            for holding in db.Holdings.find({
                'Ticker': f'{ticker}',
                'User': f'{user}'
                }):
                avg.append(holding['PricePer'])
                num_shares.append(holding['#Shares'])
            avg = np.float_(avg)
            num_shares = np.float_(num_shares)
            y =  avg_Price = sum(avg)/len(avg)
            profitPer = curr_price - avg_Price
            profit = (num_shares * curr_price) - (num_shares * avg_Price)
            print(f'You made : ${profit:.2f}')
            stocks.sale(ticker)
            ticker = 'USD'
            stocks.addholdings(profit, ticker, profitPer, num_shares)

        except Exception as e:
            print("An exception occurred ::", e)

    def s_hist():
        try:
            ticker = input('Enter stock ticker: ')
            ticker = ticker.upper()
            stockchart(ticker)

        except Exception as e:
            print("An exception occurred ::", e)

def stockchart(ticker):
    try:
        apikey =  "NQP7G8T7UX7KC6DQ"
        ts2 = TimeSeries(key=apikey, output_format='pandas')
        data = ts2.get_intraday(symbol=ticker,interval='1min', outputsize='full')
        print("index:", data.index)
        print(data)
        data[0]['4. close'].plot()
        plt.title(f'Intraday Times Series for the {ticker} stock (1 min)')
        plt.show()

    except Exception as e:
        print("An exception occurred ::", e)