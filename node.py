import time
import pexpect
import threading

PINGINTERVAL = 5

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

        # Setup latency measurment
        self.shutdown = False
        threading.Thread(target=self.start_stats, args=[]).start()

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

    def start_stats(self):
        ping_command = 'ping -i ' + str(PINGINTERVAL) + ' ' + self.ipaddr
        latency_handler = pexpect.spawn(ping_command)
        latency_handler.timeout=1200
        line =  ""
        while not self.shutdown:
            line = latency_handler.readline()

            if not line:
                continue

            if line.startswith("64"):
                self.latency = float(line[line.find(b'time=') + 5:line.find(b' ms')])
                continue

            time.sleep(1)

    def shutdown_stats(self):
        self.shutdown = True

    def to_string(self):
        return ("Node " + str(self.Id) + " @ " + str(self.ipaddr) + " " + time.asctime(self.recieved_time) + ": " \
            + str(self.latency) + ", " + str(self.bandwidth_up) + ", " + str(self.bandwidth_down))