"""This module provides OutputManager's to display Nodes to the user"""

from __future__ import print_function
import threading
import time

# The time interval in seconds which updates the display (prints out to console)
DISPLAY_UPDATE_INTERVAL_S = 5

class OutputManager(object):
    """Manages the output of nodes and statistics

    Attributes:
      nodes: The current list of Nodes.
      shutdown: If the thread should terminate
    """

    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.shutdown = False
        self.timer_thread = threading.Timer(DISPLAY_UPDATE_INTERVAL_S, self.auto_update)
        self.timer_thread.start()

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

    def auto_update(self):
        """Timer to auto-update the display if no other activity"""
        self.timer_thread = threading.Timer(DISPLAY_UPDATE_INTERVAL_S, self.auto_update)
        self.timer_thread.start()
        self.update()

    def stop(self):
        """Signal the Output Manager to shutdown"""
        self.timer_thread.cancel()
