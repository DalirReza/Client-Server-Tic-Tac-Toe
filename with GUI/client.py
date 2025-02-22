import socket
import threading
from functools import partial
from tkinter import *
import tkinter.font as font

HOST = "127.0.0.1"
PORT = 8081
GAME_TYPE = 3

# A semaphore to ensure that only one client can send message to the server at a time.
sendMessageSemaphore = threading.Semaphore(1)


# a function that changes the turn after each move.
def changeTurn(turn):
    global turnLabel
    if turn == "X":
        if shape == "O":
            turnLabel.config(text="It's your turn.")
        else:
            turnLabel.config(text="Please wait...")
        return "O"
    if shape == "X":
        turnLabel.config(text="It's your turn.")
    else:
        turnLabel.config(text="Please wait...")
    return "X"


# A protocol to send messages to the server which get a "deliverd" message to ensure that the message have been sent correctly.
def sendMessage(message):
    sendMessageSemaphore.acquire()
    theSocket.sendall(bytes(message, 'utf-8'))
    deliverdMessage = theSocket.recv(8).decode("utf-8")
    if deliverdMessage == "deliverd":
        sendMessageSemaphore.release()
    
theSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
theSocket.connect((HOST, PORT))
name = input("please enter your name: ")
theSocket.sendall(bytes(name, 'utf-8'))
serverResponce = theSocket.recv(1024).decode("utf-8")
if serverResponce == "X":
    shape = "X"
else:
    shape = "O"
oppName = theSocket.recv(1024).decode("utf-8")

turn = "X"

# A semaphore to ensure that only one button is clicked at a time.
waitForClick = threading.Semaphore(0)


# After clicking one of the buttons this function will run and puts the shape in the cell.
def clickedFunction(i):
    global turn, LISTOFBUTTONS
    btnNames[i].set(turn)
    baghi = i%GAME_TYPE+1
    taghsim = i//GAME_TYPE+1        
    s = str(baghi) + " " + str(taghsim)
    sendMessage(s)
    turn = changeTurn(turn)
    waitForClick.release()

tool = GAME_TYPE*150+300


# creating the main window for the game.
root = Tk(className=f"sudoku - {name}")
root["bg"] = "#FFFBC0"
if shape == "X":
    oppShape = "O"
else:
    oppShape = "X"
nameLabel = Label(root, text = f"You : {shape}",font=('Times 25'))
nameLabel.configure(background="#FFFBC0", fg="#ffffff")
nameLabel.place(x=tool//2-75, y=25)
oppNameLabel = Label(root, text = f"{oppName} : {oppShape}",font=('Times 25'))
oppNameLabel.configure(background="#FFFBC0", fg="#ffffff")
oppNameLabel.place(x=tool//2-75, y=70)

if shape == "X":
    nameLabel.config(fg="#000000")
    oppNameLabel.config(fg="red")
else:
    nameLabel.config(fg="red")
    oppNameLabel.config(fg="#000000")


#Set the size of the window base on the type of the game
s = str(tool) + "x" + str(tool)
root.geometry(s)
turnLabel = Label(root, text = "Turn: X",font=('Helvetica 20'), fg="#000000", bg="#FFFBC0")
turnLabel.place(x = tool//2-75, y = tool-100)
changeTurn("O")


# List of the text of each button.
btnNames = [StringVar() for _ in range(GAME_TYPE*GAME_TYPE)]
myFont = font.Font(family='Helvetica', size=100)

# A list to store all of the buttons.
LISTOFBUTTONS = []
for i in range(GAME_TYPE*GAME_TYPE):
    theBottun = Button(root, font=myFont, textvariable=btnNames[i], command=partial(clickedFunction, i), compound="bottom", justify=LEFT, state=DISABLED, background="#FFFBC0", fg="#ffffff")
    theBottun.place(x=i%GAME_TYPE*150+150, y=i//GAME_TYPE*150+150, width=150, height=150)
    LISTOFBUTTONS.append(theBottun)

# A function to change the foreground text color of the X and O in buttons.
def changeFgColor():
    for i in LISTOFBUTTONS:
        if i['text'] == "X":
            i.config(fg="#000000", disabledforeground="#000000")
        if i['text'] == "O":
            i.config(fg="red", disabledforeground="red")

# the main function to handle the client base on its turn.
def clienteHandler():
    global turn, shape, theSocket, GAME_TYPE
    while True:
        changeFgColor()
        if turn == shape:
            for button in LISTOFBUTTONS:
                if button['text'] != "X" and button['text'] != "O":
                    button.config(state=NORMAL)
            waitForClick.acquire()
            for button in LISTOFBUTTONS:
                button.config(state=DISABLED)
            serverResponce = theSocket.recv(1024).decode("utf-8")
            if serverResponce[0] == "2":
                if serverResponce[1] == shape:
                    turnLabel.config(text=f"{name} Won The Game!", fg="#000000")
                else :
                    turnLabel.config(text=f"{oppName} Won The Game!", fg="#000000")
                turnLabel.place(x = tool//2-110, y = tool-100)
        else:
            sendMessage("notMyTurn")
            serverResponce = theSocket.recv(1024).decode("utf-8")
            if serverResponce[0] == "1":
                a, b = map(int, serverResponce[1:].split())
                btnNames[(b-1)*GAME_TYPE+a-1].set(turn)
                turn = changeTurn(turn)
            elif serverResponce[0] == "2":   
                a, b = map(int, serverResponce[2:].split())
                btnNames[(b-1)*GAME_TYPE+a-1].set(turn)
                if serverResponce[1] == shape:
                    turnLabel.config(text=f"{name} Won The Game!")
                else :
                    turnLabel.config(text=f"{oppName} Won The Game!")
                turnLabel.place(x = tool//2-110, y = tool-100)
                break
    changeFgColor()
    
t = threading.Thread(target=clienteHandler)
t.start()

root.mainloop()
t.join()