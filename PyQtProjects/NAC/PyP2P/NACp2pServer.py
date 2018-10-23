from sys import argv, exit, exc_info
import socket
from threading import Thread
import random


class MainGame():
    def __init__(self):
        self.game_as_server()
        self.server = TempObj()


    def game_as_server(self):
        self.servername = input("Server Name: ")
        self.server = Server(self)

    def in_game(self):
        pass


class Server:  # Totally not stolen code...
    def __init__(self, parent):
        print("Server being made")
        self.parent = parent
        self.players = []
        self.board = {}
        self.soc = ""

        self.board_creation()
        self.start_server()


    def board_creation(self):
        for x in range(3):
            for y in range(3):
                self.board[x, y] = " "

    def processing(self, toprocess):
        print("Processing: "+ toprocess)
        result = "null"
        # r00 will return the value of the coord 0,0
        # s01X will set the value of the coord 0,1 to X
        # q will quit the game
        # f will return the full board

        if toprocess[0] == "r":
            x , y = int(toprocess[1]), int(toprocess[2])
            result = self.board[x, y]

        if toprocess[0] == "j":
            playerinfo = toprocess.split(".")
            print(playerinfo)

            self.add_player(playerinfo)

        if toprocess[0] == "f":
            result = self.board

        if toprocess[0] == "s":
            x , y = int(toprocess[1]), int(toprocess[2])
            self.board[x, y] = toprocess[3]
            result = self.board


        return (result)

    def add_player(self, playerinfo):
        self.players.append({})
        playerindex = len(self.players) - 1
        self.players[playerindex]["username"] = playerinfo[0]
        self.players[playerindex]["chr"] = playerinfo[1]
        #self.players[playerindex]["room"] = playerinfo[2]
        #self.players[playerindex]["ip"] = playerinfo[3]
        print(self.players)

    def client_thread(self, conn, ip, port):
        # the input is in bytes, so decode it
        clientinput_bytes = conn.recv(4096)

        # decode input and strip the end of line
        clientinput_string = clientinput_bytes.decode("utf8").rstrip()

        res = self.processing(clientinput_string)
        print("Result of processing is: ", res)

        vysl = res.encode("utf8")  # encode the result string
        conn.sendall(vysl)  # send it to client

    def start_server(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this is for easy starting/killing the app
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Socket created')
        binded = False
        while not binded:
            try:
                self.soc.bind(("127.0.0.1", 12345))
                print('Socket bind complete')
                binded = True
            except socket.error as msg:
                print('Bind failed. Error : ' + str(exc_info()))

        self.soc.listen(10)
        print('Socket now listening')
        accepting = True
        while True:
            self.soc.listen(10)
            print('Socket now listening')
            conn, addr = self.soc.accept()
            ip, port = str(addr[0]), str(addr[1])
            print('Accepting connection from ' + ip + ':' + port)

            Thread(target=self.client_thread, args=(conn, ip, port)).start()

        self.soc.close()


class TempObj:
    def __init__(self):
        pass

def main():
    game = MainGame()


if __name__ == '__main__':
    main()
