import socket


class Server:
    def __init__(self):
        self.domainname = ""

    def domaintoip(self):
        self.ip = socket.gethostbyname(self.domainname)
        return self.ip

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = Server()

server.domainname = "www.google.com"
print(server.domaintoip())
