# Journey (20 points, misc)
_“You unlock this door with the key of imagination. Beyond it is another dimension: a dimension of sound, a dimension of sight, a dimension of mind. You’re moving into a land of both shadow and substance, of things and ideas. You’ve just crossed over into… the Twilight Zone.”_
## Problem
Every journey starts on step ___one___

`nc p1.tjctf.org 8009`

## Solution
This was a pretty fun and simple problem.

Running the command mentioned above, we are taken to what, at first glance, a typing game?

```
$ nc p1.tjctf.org 8009
Encountered 'one'
The first step:
```
If we type what it wants for a while, it seems to go on forever...
```
The first step: one
Encountered 'infected'
The next step: infected
Encountered 'solubility'
The next step: solubility
Encountered 'sitter'
The next step: 
```
Don't mess up either.
```
Encountered 'sitter'
The next step: sitser
A step in the wrong direction!
$
```

Not knowing much Python, I could probably write a script that solves this for us.
### The Script
```Python
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
```
After running `python3 journey.py` for a while, seeing all the things you'd have to type out by hand otherwise, we see the flag at the very end:
```
one
infected
solubility
[...]
knifes
expounding
sycamore
tjctf{an\_38720\_step\_journey}
```

