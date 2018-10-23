import sys
import socket
from sys import argv, exit
from PyQt5 import QtWidgets, QtCore, QtGui


class Server:
    def __init__(self):
        print("Server created")
        self.start_server()

    def processing(self,toprocess):
        print("Processing "+toprocess)
        return (toprocess)

    def client_thread(self, conn, ip, port):
        # the input is in bytes, so decode it
        clientinput_bytes = conn.recv(4096)

        # decode input and strip the end of line
        clientinput_string = clientinput_bytes.decode("utf8").rstrip()

        res = self.processing(clientinput_string)
        print("Result of processing {} is: {}".format(clientinput_string, res))

        vysl = res.encode("utf8")  # encode the result string
        conn.sendall(vysl)  # send it to client
        conn.close()  # close connection
        print('Connection ' + ip + ':' + port + " ended")

    def start_server(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this is for easy starting/killing the app
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Socket created')

        try:
            soc.bind(("127.0.0.1", 12345))
            print('Socket bind complete')
        except socket.error as msg:
            print('Bind failed. Error : ' + str(sys.exc_info()))
            sys.exit()

        soc.listen(10)
        print('Socket now listening')

        # for handling task in separate jobs we need threading
        from threading import Thread

        # this will make an infinite loop needed for
        # not reseting server for every client
        while True:
            conn, addr = soc.accept()
            ip, port = str(addr[0]), str(addr[1])
            print('Accepting connection from ' + ip + ':' + port)

            Thread(target=self.client_thread, args=(conn, ip, port)).start()

        soc.close()



server = Server()