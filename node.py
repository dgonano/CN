import time
import pexpect
import threading
from socket import *

PINGINTERVAL = 5
BUFSIZE = 1000

class Node(object):
    # An object representing a node on the network

    # Attributes:
    #   Id: A string representing the node's identifier.
    #   ipaddr: The IP address of the node
    #   latency: The time in ms for a round trip to the node
    #   bandwidth_up: The estimated transfer rate to the node (Kb/sec)
    #   bandwidth_down: The estimated transfer rate from the node (Kb/sec)

    def __init__(self, Id, ipaddr, port, recieved_time, latency=0, bandwidth_up=0, bandwidth_down=0):
        self.Id = Id
        self.ipaddr = ipaddr
        self.port = port
        self.latency = latency
        self.bandwidth_up = bandwidth_up
        self.bandwidth_down = bandwidth_down
        self.recieved_time = recieved_time

        # Setup latency measurment
        self.shutdown = False
        threading.Thread(target=self.start_stats, args=[]).start()
        # print("Node created: " + self.to_string())

    def get_Id(self):
        return self.Id

    def get_time(self):
        return self.recieved_time

    def set_time(self, recieved_time):
        self.recieved_time = recieved_time

    def set_bandwidth_down(self, bandwidth_down=0):
        self.bandwidth_down = bandwidth_down

    def start_stats(self):
        # latency Setup
        ping_command = 'ping -i ' + str(PINGINTERVAL) + ' ' + self.ipaddr
        latency_handler = pexpect.spawn(ping_command)
        latency_handler.timeout=1200
        line =  ""
        
        # Bandwidth Up Setup
        count = 1000
        testdata = 'x' * (BUFSIZE-1) + '\n'
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.ipaddr, self.port))
        while not self.shutdown:
            # Latency
            line = latency_handler.readline()

            if line.startswith("64"):
                self.latency = float(line[line.find(b'time=') + 5:line.find(b' ms')])

            # Bandwidth Up 
            # try:
            
            s.send(self.Id)
            t1 = time.time()
            i = 0
            while i < count:
                i = i+1
                s.send(testdata)
            # s.shutdown(1) # Send EOF
            t2 = time.time()
            self.bandwidth_up = round((BUFSIZE*count*0.001) / (t2-t1), 2)
            print 'CRaw timers:', t1, t2
            print 'CIntervals:', t2-t1
            print 'CThroughput:', self.bandwidth_up, ' KB/sec.'
            # except:
                # self.bandwidth_up = 0
            
            time.sleep(5)

    def shutdown_stats(self):
        self.shutdown = True

    def to_string(self):
        return ("Node " + str(self.Id) + " @ " + str(self.ipaddr) + ":" + str(self.port) + " " + time.asctime(self.recieved_time) + ": " \
            + str(self.latency) + ", " + str(self.bandwidth_up) + ", " + str(self.bandwidth_down))