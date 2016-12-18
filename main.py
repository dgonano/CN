#! /usr/bin/env python

"""This is the main progam for the Conneciton Node.
It setups up required descovery services and output managers.

- Run the Connection Node with './main.py'
- Exit with 'ctrl-c'
"""

from __future__ import print_function
import time
import sys
import signal
import optparse
import uuid

from OutputManager import OutputManager
from DiscoveryService import DiscoveryService

# Constants
# Port used to host TCP server for bandwidth measurment
BASE_PORT = 41000
# Port used to listen for UDP broadcasts for the discovery service
DISCOVERY_PORT = 42000

# pylint: disable=C0103

# Get arguments
parser = optparse.OptionParser()
parser.add_option('-s', '--silent', \
    dest="silent", \
    action="store_true", \
    default=False, \
    help="don't display any messages")
parser.add_option('-d', '--debug', \
    dest="debug", \
    action="store_true", \
    default=False, \
    help="display debug messages")

cmdopts, cmdargs = parser.parse_args()

# Global variables
# Input options
silent = cmdopts.silent
debug = cmdopts.debug
# The UUID of this Node
uid = ''
# List of known Nodes
nodes = []
# List of services to shutdown at cleanup
services = []
# The output manager
output_manger = None
# The discovery service
discovery_service = None

# pylint: enable=C0103

def log(log_line, level=1):
    """Prints a log line to console"""
    if silent:
        return
    if level == 0 or debug:
        print(time.asctime() + "    " + log_line)

def loop():
    """Main program on the Conenction Node"""
    while True:
        # Sleep so we can capture exit signal
        time.sleep(100)

def setup():
    """Setup the Connection Node"""
    log("Setup Starting")
    global discovery_service    # pylint: disable=C0103
    global output_manger        # pylint: disable=C0103
    global uid                  # pylint: disable=C0103
    global nodes

    # Capture exit signals and run cleanup
    for sig in (signal.SIGABRT, signal.SIGILL, signal.SIGINT, \
        signal.SIGSEGV, signal.SIGTERM):
        signal.signal(sig, cleanup)

    # Generate ID
    uid = uuid.uuid4()
    log("UUID generated: " + str(uid), level=0)

    # Create Descovery Service
    discovery_service = DiscoveryService(uid, nodes, DISCOVERY_PORT)
    services.append(discovery_service)

    # Create Output Manager
    output_manger = OutputManager(nodes)
    services.append(output_manger)

def cleanup(signal, frame):
    """Ceanup all services of the Connection Node"""
    log("Shutting down Communication Node...", level=0)
    for service in services:
        service.stop()
    sys.exit(0)


if __name__ == "__main__":
    log("Setting up Communication Node...", level=0)
    setup()
    log("Communication Started", level=0)
    loop()
