import socket
import re

# https://gist.github.com/leonjza/f35a7252babdf77c8421 
class Netcat:

    """ Python 'netcat like' module """

    def __init__(self, ip, port):

        self.buff = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def read(self, length = 1024):

        """ Read 1024 bytes off the socket """

        return self.socket.recv(length)
 
    def read_until(self, data):

        """ Read data into the buffer until we have data """

        while not data in self.buff:
            self.buff += self.socket.recv(1024)
 
        pos = self.buff.find(data)
        rval = self.buff[:pos + len(data)]
        self.buff = self.buff[pos + len(data):]
 
        return rval
 
    def write(self, data):

        self.socket.send(data)
    
    def close(self):

        self.socket.close()

if __name__ == '__main__':
    nc = Netcat('p1.tjctf.org', 8009)
    while True:
        nc.buff = b''
        string = nc.read_until(b"\n")
        string = string.decode("utf-8")
        string = re.findall(r"\'(.*)\'", string)
        string = ' '.join(string)
        print(string)
        string += "\n"
        string = str.encode(string)
        nc.write(string)
