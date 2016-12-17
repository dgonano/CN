"""This module provies the Node object, used to represent
a single Node on the network
"""

import time
import threading

import pexpect

# How often it pings the Communicaion node to meansure latency
PING_INTERVAL = 5

class Node(object):
    """ An object representing a node on the network

    Attributes:
      uid: The node's identifier.
      ipaddr: The IP address of the node
      recieved_time: The time of last contact with the node
      latency: The time in Ms for a round trip to the node
      bandwidth_up: The estimated transfer rate to the node (KB/sec)
      bandwidth_down: The estimated transfer rate from the node (KB/sec)
    """
    def __init__(self, uid, ipaddr, recieved_time):
        self.uid = uid
        self.ipaddr = ipaddr
        self.recieved_time = recieved_time
        self.latency = 0
        self.bandwidth_up = 0
        self.bandwidth_down = 0

        # Setup latency measurment
        self.shutdown = False
        threading.Thread(target=self.start_stats, args=[]).start()

    def get_id(self):
        """Return the uuid of the Node"""
        return self.uid

    def get_time(self):
        """Returns the time the Node was last seen"""
        return self.recieved_time

    def set_time(self, recieved_time):
        """Set the time the Node was last seen"""
        self.recieved_time = recieved_time

    def set_stats(self, latency=0, bandwidth_up=0, bandwidth_down=0):
        """Update the Nodes network stats"""
        self.latency = latency
        self.bandwidth_up = bandwidth_up
        self.bandwidth_down = bandwidth_down

    def start_stats(self):
        """Method to start the Nodes stats calculations, run as a thread"""
        # Setup underlying ping program
        ping_command = 'ping -i ' + str(PING_INTERVAL) + ' ' + self.ipaddr
        latency_handler = pexpect.spawn(ping_command)
        latency_handler.timeout = 1200
        line = ""
        # Continually read lines from the program
        while not self.shutdown:
            line = latency_handler.readline()

            if not line:
                continue

            if line.startswith("64"):
                latency_str = line[line.find(b'time=') + 5:line.find(b' ms')]
                self.latency = float(latency_str)
                # Continue immidiatly to ensure we have the latest measurment
                continue

            time.sleep(1)

    def shutdown_stats(self):
        """Signals the Node to stop to clear memory"""
        self.shutdown = True

    def to_string(self):
        """Returns a string representation of the Node"""
        return "Node " + str(self.uid) + " @ " + str(self.ipaddr) + " " \
            + time.asctime(self.recieved_time) + ": " \
            + str(self.latency) + "ms, " + str(self.bandwidth_up) \
            + ", " + str(self.bandwidth_down)
