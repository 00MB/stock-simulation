#Python stock market simulator
from globals import *


print(f"""\nThis is a real time investment simulation. \n
If you are new or want to reset the simulation, \ntype !START, otherwhise type !CONTINUE. \n
To see a list of commands, type !COMMANDS {line}""")

def start():
        fundstart = input("Enter your starting amount(GBP): ")
        print("Unknown error")
    if not type(fundstart) is int:
        return

def quit():
    exit()

def commands():
    print("""
!START - clears data and prompts user to enter starting funds amount\n
!QUIT - stops the process and closes the application\n
!BUY - displays menu to buy stocks\n
!SELL - displays menu to sell your current stocks\n
!STOCKS - displays the currently owned stocks\n
!PRICE {stock symbol} - displays live price of stock\n
!FUNDS - displays the current funds available\n
!ABOUT - displays information about the program and creator\n
    """)

globals = {'!START' : start, '!QUIT' : quit, '!COMMANDS' : commands}

while True:
        inp = input("Enter command: ")
    if inp in globals:
        print("correct")
        print(line)
        globals[inp]()
    else:
        print("ERROR - invalid command")

#main program
#getinput() = fundstart
