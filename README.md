# PaperTrader

basic cli paper trader written in python using mongodb to store stock purchases.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is a command line interface paper trader written in python. It takes real time stock data from two diffent free api's [finnhub](https://finnhub.io/) to get real time stock data. [Alphavantage](https://www.alphavantage.co) to get historical data.
	
## Technologies
Project is created with:
* collections: Counter 
* numpy 
* termcolor: colored
* finnhub
* datetime
* requests
* os
* json
* bson: ObjectId
* matplotlib
* mongo db
* alpha_vantage
	
## Setup
To run this project clone it from git hub and run main.py:

Step 1:
```
run mongo bat file
```
Step 2:
```
$ pip install numpy
$ pip install finnhub-python
$ pip install matplotlib
$ pip install alpha_vantage
$ pip install termcolor
$ pip install mongo db
$ pip install requests
```
Step 3:
```
$ cd ../prod1
$ python main.py
```
