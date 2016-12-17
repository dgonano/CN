import threading
import time
import uuid
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname, SO_REUSEPORT

from node import Node

class DiscoveryService(threading.Thread):
    # Manages the discovery service

    # Attributes:
    #   port: UDP port to broadcast too
    #   shutdown: If the thread should terminate
    #   nodes: List of currently known nodes
    #   bandwidth_port: Port to broadcast to other nodes

    def __init__(self, Id, bandwidth_port, port=42000):
        threading.Thread.__init__(self)
        self.port = port
        self.Id = Id
        self.bandwidth_port = bandwidth_port
        self.shutdown = False
        self.nodes = []

    def run(self):
        # Start broadcast thread
        threading.Thread(target=self.broadcast, args=[]).start()

        # Setup recieving socket
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET,SO_REUSEPORT, 1)
        s.bind(('', self.port))

        while not self.shutdown:
            new = True

            data, addr = s.recvfrom(1024) #wait for a packet
            datas = data.split(",", 2)
            if (datas[0] == str(self.Id)):
                new = False
            else:
                for n in self.nodes:
                    # If it's already in the list, just update the time.
                    if (datas[0] == n.get_Id()):
                        n.set_time(time.localtime())
                        new = False
            
            # If it's timed out, remove it.
            current_time = time.mktime(time.localtime())
            for n in list(self.nodes):
                if (current_time - time.mktime(n.get_time()) > 30):
                    # Stop the stats thread for that Node and remove it
                    n.shutdown_stats()
                    self.nodes.remove(n)

            # New node, add it to the list. 
            if new:
                self.nodes.append(Node(datas[0], addr[0], int(datas[1]), time.localtime()))

    def getNodes(self):
        return self.nodes

    def broadcast(self):
        s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
        s.bind(('', 0))
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket

        loop = 0
        while not self.shutdown:
            loop = loop + 1

            if (loop == 5):
                loop = 0
                data = str(self.Id) + "," + str(self.bandwidth_port)
                s.sendto(data, ('<broadcast>', self.port))
            
            time.sleep(1)

    def stop(self):
        self.shutdown = True

    def stopped(self):
        return self.shutdown