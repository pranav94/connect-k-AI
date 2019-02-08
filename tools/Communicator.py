from subprocess import Popen, PIPE
import select
import fcntl, os
import time

class Communicator(object):
    def __init__(self, command,timeout):
        self.timeout = timeout
        self.process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        flags = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)
        fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    def send(self, data, tail = '\n'.encode()):
        self.process.stdin.write(data + tail)
        self.process.stdin.flush()
        time.sleep(0.01)

    def recv(self,t=0.2):
        r = ''
        pr = self.process.stdout
        per = self.process.stderr
        bt = time.time()
        er = b''
        while (time.time() - bt < self.timeout):
            if not select.select([pr], [], [], 0)[0]:
                time.sleep(t)
                continue

            r = pr.read().rstrip()
            if r.decode() == ' ' or r.decode() == '':
                er = per.read()
            return r,er
        raise TimeoutError