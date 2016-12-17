import threading
import time
from socket import *

from node import Node

IDLENGTH = 36
BUFSIZE = 1024

class BandwidthServer(threading.Thread):
    # Manages TCP server used for measuring bandwidth

    # Attributes:
    #   port: TCP port it's listening on
    #   shutdown: If the thread should terminate

    def __init__(self, port=41000):
        threading.Thread.__init__(self)
        self.port = port
        self.started = False
        self.shutdown = False
        self.bandwidths_down = []

    # Udate the nodes with the latest bandwidth down measurment
    def update_nodes(self, nodes):
        for n in nodes:
            for b in self.bandwidths_down:
                if (b[0] == n.get_Id()):
                    n.set_bandwidth_down(b[1])
        return nodes

    def is_started(self):
        return self.started

    def get_port(self):
        return self.port

    def run(self):
        s = socket(AF_INET, SOCK_STREAM)
        bound = False
        while not bound:
            try:
                s.bind(('', self.port))
                bound = True
            except: 
                self.port = self.port +1
                continue
        self.started = True

        s.listen(1)
        print('TCP Bandwidth Server ready... ' + str(self.port))
        while not self.shutdown:
            conn, (host, remoteport) = s.accept()
            Id = conn.recv(IDLENGTH)
            print(Id)
            t1 = time.time()
            count = 0
            while True:
                data = conn.recv(BUFSIZE)
                # print(data)
                if not data:
                    print("Finished Recieving")
                    break
                del data
                count = count+1

            t2 = time.time()
            conn.send('OK\n')
            conn.close()
            speed = round((BUFSIZE*count*0.001) / (t2-t1), 2)
            print 'SRaw timers:', t1, t2
            print 'SIntervals:', t2-t1
            print 'SThroughput: ', Id, " ", speed,' KB/sec.'
            print 'SDone with', host, 'port', remoteport
            # Update list of IDs
            for n in list(self.bandwidths_down):
                if (n[0] == Id):
                    self.bandwidths_down.remove(n)
            self.bandwidths_down.append((Id, speed))
            print(self.bandwidths_down)


    def stop(self):
        self.shutdown = True

    def stopped(self):
        return self.shutdown