#Python stock market simulator
fileread = open("data.txt", "r")
from globals import *
from bs4 import BeautifulSoup
import requests

funds = float(fileread.readline())
portfolio = fileread.readline().strip().split(",")
for x in range(len(portfolio)):
    portfolio[x] = portfolio[x].split("-")
    portfolio[x][1] = float(portfolio[x][1])
    portfolio[x][2] = int(portfolio[x][2])

print(f"""\nThis is a real time investment simulation. \n
If you are new or want to reset the simulation, type !START. \n
To see a list of commands, type !COMMANDS {line}""")

#FUNCTIONS

def buy():
    global funds
    global portfolio
    symbol = input("Enter stock symbol: ")
    url = "https://uk.finance.yahoo.com/quote/" + symbol
    #url = "https://uk.finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch"
    print(url)
    headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36"}
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, 'html.parser')
    try:
        price = float(soup.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").get_text())
    except:
        print("ERROR - invalid stock symbol")
        return
    print(f"Stock price: ${price}")
    print(f"funds available: ${funds}")
    try:
        amount = int(input("Please insert stock amount (To cancel, insert 0): "))
    except ValueError:
        print("\nERROR - incorrect data type")
        return
    if amount < 0 or amount > 1000:
        print("ERROR - unavailable amount")
        return
    elif amount == 0:
        return
    totalsum = amount * price
    if totalsum > funds:
        print("Costs exceeds available funds")
        return
    else:
        portfolio.append([symbol,price,amount])
        funds -= totalsum
        print("Successfully purchased stock")

def fund():
    print(f"Current funds available: {funds}")

def stocks():
    print("Current stocks:")
    for x in portfolio:
        print(f"Symbol: {x[0]}, Bought at: ${x[1]}, Amount: {x[2]}")

def start():
    global funds
    global portfolio
    try:
        funds = float(input("Enter your starting amount: $"))
    except ValueError:
        print("\nERROR - incorrect data type")
        return
    print("\nSuccessfully set funds")
    portfolio = []

def quit():
    exit()

def commands():
    print("""
!ABOUT - displays information about the program and creator\n
!BUY - displays menu to buy stocks\n #
!FUND - displays the current funds available\n #
!PRICE {stock symbol} - displays live price of stock\n
!QUIT - stops the process and closes the application\n
!SAVE - saves current stocks and available funds\n
!SELL - displays menu to sell your current stocks\n
!START - clears data and prompts user to enter starting funds amount\n #
!STOCKS - displays the currently owned stocks\n #
    """)

globals = {'!BUY' : buy, '!START' : start, '!QUIT' : quit, '!COMMANDS' : commands, '!STOCKS' : stocks, '!FUND' : fund}

while True:
    inp = input("Enter command: ")
    if inp in globals:
        print("\n")
        globals[inp]()
        print(line)
    else:
        print("ERROR - invalid command")
