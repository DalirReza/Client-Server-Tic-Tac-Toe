import threading
import socket

GAME_TYPE = 3 #The size of the Board


#A list to sotre the current position of the game based on the latest moves.
myList = [["--" for _ in range(GAME_TYPE)] for _ in range(GAME_TYPE)] 


#A function to check win condition for 5*5 mode.
def fiveCheack(n, a1, b1, a2, b2):
    if n != 5:
        return True
    if myList[a1][b1] == myList[a2][b2]:
        return True
    return False


#The main function to check if someone won yet or not.
def checkWin(n):
    if n == 3 or n == 4:
        cond = 3
    else:
        cond = 4
    for i in range(n):
        if (myList[i].count("X") >= cond or myList[i].count("O") >= cond) and myList[i][1] == myList[i][2] and fiveCheack(n, i, 2, i, 3):
            return myList[i][1]

    for i in range(n):
        x = 0
        for j in range(n-1):
            if myList[j][i] == myList[j+1][i] and  myList[j][i] != "--":
                x += 1
        if x >= cond-1 and myList[1][i] == myList[2][i] and fiveCheack(n, 2, i, 3, i):
            return myList[1][i]

    x = 0
    for i in range(n-1):
        if myList[i][i] == myList[i+1][i+1]:
            x += 1
    if x >= cond-1 and myList[1][1] == myList[2][2] and myList[1][1] != "--" and fiveCheack(n, 2, 2, 3, 3):
        return myList[1][1]

    x = 0
    for i in range(n-1):
        if myList[i][n-i-1] == myList[i+1][n-i-2]:
            x += 1
    if x >= cond-1 and myList[1][n-2] == myList[2][n-3] and myList[1][n-2] != "--" and fiveCheack(n, 2, n-3, 3, n-4):
        return myList[1][n-2]
    return False
    
    
#the function that controls the game while playing with each other.
def clientHandler(connection, clientName, connection2, clientName2):
    global myList
    connection.sendall(bytes(clientName2, 'utf-8'))
    connection2.sendall(bytes(clientName, 'utf-8'))
    while True:
        m1 = connection.recv(1024).decode("utf-8")
        connection.sendall(bytes("deliverd", 'utf-8'))
        m2 = connection2.recv(1024).decode("utf-8")
        connection2.sendall(bytes("deliverd", 'utf-8'))
        if m1 == "notMyTurn":
            a, b = map(int, m2.split())
            myList[a-1][b-1] = "O"
            whoWon = checkWin(GAME_TYPE)
            if whoWon != False:
                connection.sendall(bytes("2"+whoWon+m2, 'utf-8'))
                connection2.sendall(bytes("2"+whoWon, 'utf-8'))
                break
            connection2.sendall(bytes("continue", 'utf-8'))
            connection.sendall(bytes("1"+m2, 'utf-8'))
        else:
            a, b = map(int, m1.split())
            myList[a-1][b-1] = "X"
            whoWon = checkWin(GAME_TYPE)
            if whoWon != False:
                connection.sendall(bytes("2"+whoWon, 'utf-8'))
                connection2.sendall(bytes("2"+whoWon+m1, 'utf-8'))
                break
            connection.sendall(bytes("continue", 'utf-8'))
            connection2.sendall(bytes("1"+m1, 'utf-8'))    
    return

HOST = "127.0.0.1"
PORT = 8081
theSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
theSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
theSocket.bind((HOST, PORT))
theSocket.listen()

numberOfGames = 0


# if two client connect to the server they will get matched and start playing with each other
# and server still listens for another to players to connect them.
while True:    
    connection, address = theSocket.accept()
    clientName = connection.recv(1024).decode("utf-8")
    connection.sendall(bytes("X", 'utf-8'))
    print("waiting for someone to join the game...")
    
    connection2, address2 = theSocket.accept()
    clientName2 = connection2.recv(1024).decode("utf-8")
    connection2.sendall(bytes("O", 'utf-8'))
    print("both connected")
    
    t = threading.Thread(target=clientHandler, args=[connection, clientName, connection2, clientName2])
    t.start()
    numberOfGames += 1