import time

class Node(object):
    # An object representing a node on the network

    # Attributes:
    #   Id: A string representing the node's identifier.
    #   ipaddr: The IP address of the node
    #   latency: The time in ms for a round trip to the node
    #   bandwidth_up: The estimated transfer rate to the node (Kb/sec)
    #   bandwidth_down: The estimated transfer rate from the node (Kb/sec)

    def __init__(self, Id, ipaddr, recieved_time, latency=0, bandwidth_up=0, bandwidth_down=0):
        self.Id = Id
        self.ipaddr = ipaddr
        self.latency = latency
        self.bandwidth_up = bandwidth_up
        self.bandwidth_down = bandwidth_down
        self.recieved_time = recieved_time

    def get_Id(self):
        return self.Id

    def get_time(self):
        return self.recieved_time

    def set_time(self, recieved_time):
        self.recieved_time = recieved_time

    def set_stats(self, latency=0, bandwidth_up=0, bandwidth_down=0):
        self.latency = latency
        self.bandwidth_up = bandwidth_up
        self.bandwidth_down = bandwidth_down

    def to_string(self):
        return ("Node " + str(self.Id) + " @ " + str(self.ipaddr) + " " + time.asctime(self.recieved_time) + ": " \
            + str(self.latency) + ", " + str(self.bandwidth_up) + ", " + str(self.bandwidth_down))