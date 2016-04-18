import socket
import threading
import unified
import sys

class User:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self,adress,port):
        self.adress = adress
        self.port = port

    def connect(self):
        self.s.connect((self.adress,self.port))
        msg = '''WRITE user.py
working-directory:home/pi/Documents/Python Projects/ZFTP
selected-disk:E
anotherArgument01:argument02
write-type:overwrite

some data'''
        self.s.send(msg.encode())
        msg = self.s.recv(2048).decode('utf-8')
        print(unified.decode(msg))

if __name__ == '__main__':
    client = User(sys.argv[1], 1919)
    client.connect()


