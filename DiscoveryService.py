"""This module provides a Discovery Service to help discover
Nodes on the network
"""

import threading
import time
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, \
    SO_BROADCAST, SO_REUSEPORT

from Node import Node

# How often to broadcst in seconds
BROADCAST_INTERVAL_S = 5
# Default discovry port
DEFAULT_BROADCAST_PORT = 42000
# Time before a node is declared as no longer avalible in seconds
NODE_TIMEOUT_S = 30

class DiscoveryService(threading.Thread):
    """This Module sets up and manages the discovery service

    Attributes:
      uid: The uuid of this connumication node
      port: UDP port to broadcast too
      shutdown: If the thread should terminate
      nodes: List of currently known nodes
    """

    def __init__(self, uid, port=DEFAULT_BROADCAST_PORT):
        threading.Thread.__init__(self)
        self.port = port
        self.uid = uid
        self.shutdown = False
        self.nodes = []

    def run(self):
        """Start the DiscoveryService"""
        # Start broadcast thread
        threading.Thread(target=self.broadcast, args=[]).start()

        # Setup recieving socket
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        sock.bind(('', self.port))

        # continually monitor for incoming service broadcasts
        while not self.shutdown:
            new = True

            # wait for a packet
            data, addr = sock.recvfrom(1024)
            # Check if it's from this node first
            if data == str(self.uid):
                new = False
            else:
                for node in self.nodes:
                    # If it's already in the list, just update the time.
                    if data == node.get_id():
                        node.set_time(time.localtime())
                        new = False

            # If it's timed out, remove it.
            current_time = time.mktime(time.localtime())
            for node in list(self.nodes):
                if current_time - time.mktime(node.get_time()) > NODE_TIMEOUT_S:
                    # Stop the stats thread for that Node and remove it
                    node.shutdown_stats()
                    self.nodes.remove(node)

            # New node, add it to the list.
            if new:
                self.nodes.append(Node(data, addr[0], time.localtime()))

    def get_nodes(self):
        """Return currently known nodes"""
        return self.nodes

    # Continually braodcast UPD notification packets for other nodes
    def broadcast(self):
        """Method to run the broadcast part of the service, run as a thread"""
        sock = socket(AF_INET, SOCK_DGRAM) #create UDP socket
        sock.bind(('', 0))
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket

        loop = 0
        while not self.shutdown:
            loop = loop + 1

            if loop == BROADCAST_INTERVAL_S:
                loop = 0
                data = str(self.uid)
                # Try to send it
                try:
                    sock.sendto(data, ('<broadcast>', self.port))
                except:
                    pass

            time.sleep(1)

    def stop(self):
        """Signal the Discovery service to shutdown"""
        self.shutdown = True
