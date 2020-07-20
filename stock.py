#Python stock market simulator
line = "\n" + "_" * 50 + "\n"

print(f"""\nThis is a real time investment simulation. \n
If you are new or want to reset your funds, \ntype !START, otherwhise type !CONTINUE. \n
To see a list of commands, type !COMMANDS {line}""")

def getinput():
    fundstart = int(input("Enter your starting amount(GBP): "))

def commands():
    print("""
    !START - clears data and prompts user to enter starting funds amount \n
    !QUIT - stops the process and closes the application \n
    !HELP -  displays \n
    !ABOUT - displays information about the program and creator \n
    """)

#main program
getinput()
commands()
