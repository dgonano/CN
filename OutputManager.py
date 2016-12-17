"""This module provides OutputManager's to display Nodes to the user"""

from __future__ import print_function
import threading
import time

# The time interval in seconds which updates the display (prints out to console)
DISPLAY_UPDATE_INTERVAL_S = 15

class OutputManager(threading.Thread):
    """Manages the output of nodes and statistics

    Attributes:
      nodes: The current list of Nodes.
      shutdown: If the thread should terminate
    """

    def __init__(self, nodes=[]):
        threading.Thread.__init__(self)
        self.nodes = nodes
        self.shutdown = False

    def run(self):
        """Start the Output Manager running"""
        loop = 0
        while not self.shutdown:
            loop = loop + 1

            if loop == DISPLAY_UPDATE_INTERVAL_S:
                loop = 0
                self.update()

            time.sleep(1)

    def get_nodes(self):
        """Return Nodes the Output Manager knows about"""
        return self.nodes

    def set_nodes(self, nodes):
        """Set the Nodes for the Output Manager to display"""
        self.nodes = nodes

    def update(self):
        """Update the display (prints to console)"""
        print ('*' * 100)
        print("     UUID                                   IP Address  " + \
            "Time                     latency, up, down")
        for node in self.nodes:
            print(node.to_string())

    def stop(self):
        """Signal the Output Manager to shutdown"""
        self.shutdown = True
