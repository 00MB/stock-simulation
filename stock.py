#Python stock market simulator

from globals import *
from bs4 import BeautifulSoup
import requests

def set():
    global portfolio
    global funds
    fileread = open("data.txt", "r")
    funds = fileread.readline()
    funds = float(funds.strip())
    portfolio = fileread.readline().strip().split(",")
    if portfolio != [""]:
        for x in range(len(portfolio)):
            portfolio[x] = portfolio[x].split("-")
            portfolio[x][1] = float(portfolio[x][1])
            portfolio[x][2] = int(portfolio[x][2])
    fileread.close()
    for x in range(len(portfolio)):
        if portfolio[x] == "":
            del portfolio[x]
set()

print(f"""\nThis is a real time investment simulation. \n
If you are new or want to reset the simulation, type !START. \n
To see a list of commands, type !COMMANDS {line}""")

#FUNCTIONS
def about():
    print("""
This stock simulator is a weekend project created by github user 00MB
on 20/7/20. The simulator works by scraping live figures from yahoo finance, and saving
the user into a text file. Feel free to play around and break it.
    """)


def buy():
    global funds
    global portfolio
    symbol = input("Enter stock symbol: ")
    url = "https://uk.finance.yahoo.com/quote/" + symbol
    headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36"}
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, 'html.parser')
    try:
        price = soup.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").get_text()
        price = float(price.replace(',',''))
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
        funds = round((funds - totalsum),2)
        print("Successfully purchased stock")

def sell():
    global funds
    global portfolio
    try:
        symbol = input("Enter stock symbol to sell: ")
        names = [x[0] for x in portfolio]
        index = names.index(symbol)
        print(f"index:{index}")
    except:
        print(f"ERROR - no {symbol} stock is owned")
        return
    print(f"Amount owned: {portfolio[index][2]}")
    try:
        amount = int(input("Input amount of stocks to sell: "))
    except ValueError:
        print("\nERROR - incorrect data type")
        return
    if amount > portfolio[index][2]:
        print("ERROR - invalid input")
        return
    url = "https://uk.finance.yahoo.com/quote/" + symbol
    headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36"}
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, 'html.parser')
    price = soup.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").get_text()
    price = float(price.replace(',',''))
    print(f"Stock bought at: ${portfolio[index][1]}")
    print(f"Current stock price: ${price}")
    print(f"Profit/loss: ${amount * (float(price) - float(portfolio[index][1]))}\n")
    sold = input(f"Would you like to sell {symbol} stock at ${price} (type Y or N): ")
    if sold.lower() == "n":
        print("Request cancelled")
        return
    elif sold.lower() == "y":
        pass
    else:
        print("ERROR - invalid input")
        return
    amountnew = portfolio[index][2] - amount
    funds = round((funds + (float(price) * amount)),2)
    if amountnew == 0:
        del portfolio[index]
    else:
        portfolio[index][2] = amountnew
    print(f"Successfully sold {symbol} stock at ${price}, your funds available are ${funds}")
    if funds < 0:
        print("\nFunds available have reached less than 0, please type !START to reset")

def fund():
    print(f"Current funds available: ${funds}")

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
    dup = portfolio
    filewrite = open("data.txt", "w")
    filewrite.write(str(funds)+"\n")
    for x in range(len(dup)):
        dup[x][1] = str(dup[x][1])
        dup[x][2] = str(dup[x][2])
        dup[x] = "-".join(dup[x])
    dup = ",".join(dup)
    filewrite.write(dup)
    filewrite.close()
    exit()

def save():
    dup = portfolio
    filewrite = open("data.txt", "w")
    filewrite.write(str(funds))
    filewrite.write("\n")
    for x in range(len(dup)):
        dup[x][1] = str(dup[x][1])
        dup[x][2] = str(dup[x][2])
        dup[x] = "-".join(dup[x])
    dup = ",".join(dup)
    filewrite.write(dup)
    filewrite.close()
    set()

def commands():
    print("""
!ABOUT - displays information about the program and creator\n
!BUY - displays menu to buy stocks\n #
!FUND - displays the current funds available\n #
!PRICE {stock symbol} - displays live price of stock\n
!QUIT - stops the process and closes the application\n
!SAVE - saves current stocks and available funds\n
!SELL - displays menu to sell your current stocks\n #
!START - clears data and prompts user to enter starting funds amount\n #
!STOCKS - displays the currently owned stocks\n #
    """)

globals = {'!BUY' : buy, '!START' : start, '!QUIT' : quit, '!COMMANDS' : commands, '!STOCKS' : stocks, '!FUND' : fund, '!SELL' : sell, '!SAVE' : save, '!ABOUT' : about}

while True:
    inp = input("Enter command: ")
    if inp in globals:
        print("\n")
        globals[inp]()
        print(line)
    else:
        print("ERROR - invalid command")
