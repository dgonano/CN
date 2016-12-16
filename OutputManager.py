import threading
import time

from node import Node

class OutputManager(threading.Thread):
    # Manages the output of nodes and statistics

    # Attributes:
    #   nodes: A list of Nodes.
    #   shutdown: If the thread should terminate

    def __init__(self, nodes=[]):
        threading.Thread.__init__(self)
        self.nodes = nodes
        self.shutdown = False

    def run(self):
        loop = 0
        while True:
            # Shutdown if required
            if self.shutdown:
                return

            loop = loop + 1 
            if (loop == 15):
                loop = 0
                self.update()

            time.sleep(1)

    def getNodes(self):
        return self.nodes

    def setNodes(self, nodes):
        self.nodes = nodes

    def update(self):
        print '*' * 100
        print("     UUID                                   IP Address  Time                     latency, up, down")
        for i in self.nodes:
            print(i.to_string())

    def stop(self):
        self.shutdown = True

    def stopped(self):
        return self.shutdown