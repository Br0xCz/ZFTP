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
        msg = '''GETFILE untitled.blend
working-directory:home/pi/Documents/Python Projects/ZFTP
selected-disk:E
anotherArgument01:argument02
write-type:overwrite

some data'''
        msg_win='''GETFILE The.Martian.2015.1080p.BluRay.CZ.AC3.x264-HdF.mkv
working-directory:Stahování
selected-disk:E
anotherArgument01:argument02
write-type:overwrite

Test text, see if that shit works, probably na'''

        self.s.send(msg_win.encode())
        msg = self.s.recv(4096).decode('utf-8')
        #print(unified.decode(msg))
        self.s.close()

if __name__ == '__main__':
    client = User(sys.argv[1], 1919)
    client.connect()


