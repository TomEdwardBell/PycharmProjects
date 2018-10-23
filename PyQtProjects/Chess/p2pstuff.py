import socket
import threading

LOCALHOST = '127.0.0.1'
BUFFER_SIZE = 1024

def main():
    class ChatListener(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.port = None

        def run(self):
            listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_socket.bind((LOCALHOST, self.port))
            listen_socket.listen(1)

            while True:

                connection, address = listen_socket.accept()

                print("Established connection with: ", address)

                message = connection.recv(BUFFER_SIZE)
                print("Them: ", message)

    class ChatSender(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.address = None
            self.port = None

        def run(self):
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.connect((self.address, self.port))

            while True:

                message = input("You: ")

                if message.lower() == "quit":
                    break
                else:
                    try:
                        send_socket.sendall(message)
                    except:
                        Exception

    ip = input("Please enter the address you would like to connect on: ")
    port = int(input("Please enter the port you would like to connect on: "))

    chat_listener = ChatListener()
    chat_listener.port = port
    chat_listener.start()

    chat_sender = ChatSender()
    chat_seernder.address = ip
    chat_sender.port = port
    chat_sender.start()

if __name__ == "__main__":
    main()