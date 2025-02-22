import socket
import threading
HOST = "127.0.0.1"
PORT = 8081
GAME_TYPE = 3

def printTheList(theList):
    for i in range(GAME_TYPE):
        for j in range(GAME_TYPE):
            print(theList[i][j], end='\t')
        print()

def changeTurn(turn):
    if turn == "X":
        return "O"
    return "X"

sem = threading.Semaphore(1)

theSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
theSocket.connect((HOST, PORT))
name = input("please enter your name: ")
theSocket.sendall(bytes(name, 'utf-8'))
serverResponce = theSocket.recv(1024).decode("utf-8")
print(f"you are playing as: {serverResponce}.")
if serverResponce == "X":
    shape = "X"
else:
    shape = "O"
oppName = theSocket.recv(1024).decode("utf-8")
print(f"you are connected to play with {oppName}.")

myList = [["--" for _ in range(GAME_TYPE)] for _ in range(GAME_TYPE)]
printTheList(myList)
turn = "X"
while True:
    if turn == shape:
        s = input(f"it's your turn. please send the location where u want to put {shape}: ")
        a, b = map(int, s.split())
        sem.acquire()
        theSocket.sendall(bytes(s, "utf-8"))
        deliverdMessage = theSocket.recv(1024).decode("utf-8")
        if deliverdMessage == "deliverd":
            sem.release()
        myList[a-1][b-1] = shape
        printTheList(myList)
        turn = changeTurn(turn)
        sem.acquire()
        deliverdMessage = theSocket.recv(1024).decode("utf-8")
        if deliverdMessage != "continue":
            sem.release()
            print(f"{deliverdMessage[1]} WON!")
            break
        else:
            sem.release()
    else:
        print("please wait while the opponent decides...")
        sem.acquire()
        theSocket.sendall(bytes("notMyTurn", "utf-8"))
        deliverdMessage = theSocket.recv(1024).decode("utf-8")
        if deliverdMessage == "deliverd":
            sem.release()
        serverResponce = theSocket.recv(1024).decode("utf-8")
        if serverResponce[0] == "1":
            a, b = map(int, serverResponce[1:].split())
            myList[a-1][b-1] = turn
            turn = changeTurn(turn)
            printTheList(myList)
        elif serverResponce[0] == "2":
            print(f"{serverResponce[1]} WON!")
            break
    