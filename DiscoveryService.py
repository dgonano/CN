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
# Interval that nodes validity is checked
NODE_CHECK_INTERVAL_S = 5

class DiscoveryService(object):
    """This Module sets up and manages the discovery service

    Attributes:
      uid: The uuid of this connumication node
      port: UDP port to broadcast too
      shutdown: If the thread should terminate
      nodes: List of currently known nodes
    """

    def __init__(self, uid, nodes, port=DEFAULT_BROADCAST_PORT):
        self.shutdown = False
        self.uid = uid
        self.nodes = nodes
        self.port = port

        # Start a timer to remove old nodes
        self.remove_old_nodes()

        # Setup Broadcast socket with Timer
        self.broadcast_sock = socket(AF_INET, SOCK_DGRAM) #create UDP socket
        self.broadcast_sock.bind(('', 0))
        self.broadcast_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.broadcast()

        # Setup Recieving
        rthread = threading.Thread(target=self.listen)
        rthread.daemon = True
        rthread.start()

    def listen(self):
        """Start the DiscoveryService"""
        # Start broadcast thread
        # threading.Thread(target=self.broadcast, args=[]).start()

        

        # Setup recieving socket
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        sock.bind(('', self.port))

        # continually monitor for incoming service broadcasts
        while not self.shutdown:
            # wait for a packet
            data, addr = sock.recvfrom(1024)

            # Check if it's from this node first
            if data == str(self.uid):
                continue
            # Check if it's already in the list
            if self.update_time(data):
                continue

            # New node, add it to the list.
            self.nodes.append(Node(data, addr[0], time.localtime()))

    def update_time(self, node_id):
        """If the node already exits, update the time
        Returns
            True: If exists and updated
            False: Doesn't exists
        """
        for node in self.nodes:
            if node_id == node.get_id():
                # It's already in the list, just update the time.
                node.set_time(time.localtime())
                return True
        # Node not found
        return False

    def remove_old_nodes(self):
        """Starts a timer that removes old nodes"""
        self.nodes_timer = threading.Timer(NODE_CHECK_INTERVAL_S, self.remove_old_nodes)
        self.nodes_timer.start()
        
        # If it's timed out, remove it.
        current_time = time.mktime(time.localtime())
        for node in list(self.nodes):
            if current_time - time.mktime(node.get_time()) > NODE_TIMEOUT_S:
                # Stop the stats thread for that Node and remove it
                node.shutdown_stats()
                self.nodes.remove(node)

    def get_nodes(self):
        """Return currently known nodes"""
        return self.nodes

    def broadcast(self):
        """Method to run the broadcast part of the service, run as a thread"""
        self.broadcast_timer = threading.Timer(BROADCAST_INTERVAL_S, self.broadcast)
        self.broadcast_timer.start()

        self.broadcast_sock.sendto(str(self.uid), ('<broadcast>', self.port))

    def stop(self):
        """Signal the Discovery service to shutdown"""
        self.shutdown = True
        self.broadcast_timer.cancel()
        self.nodes_timer.cancel()
