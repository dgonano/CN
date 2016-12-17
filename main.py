#! /usr/bin/env python

from __future__ import print_function
import importlib
import os
import time
import sys
import signal
import threading
import requests
import optparse
import uuid

from node import Node
from OutputManager import OutputManager
from DiscoveryService import DiscoveryService
from BandwidthServer import BandwidthServer

# Get arguments
parser = optparse.OptionParser()
parser.add_option('-s', '--silent',
		dest="silent",
		action="store_true",
		default=False,
		help="don't display any messages")
parser.add_option('-d', '--debug',
		dest="debug",
		action="store_true",
		default=False,
		help="display debug messages")

cmdopts, cmdargs = parser.parse_args()
silent = cmdopts.silent
debug = cmdopts.debug

# constants
DISCOVERY_PORT = 42000
BASE_PORT = 41000

# global variables
Id = ''
nodes = []
threads = []

def log(log, level=1):
	if silent:
		return
	if level == 0 or debug:
		print(time.asctime() + "    " + log)

def loop():
	while True:
		log("Main Loop Starting")

		# Get latest set of Nodes
		nodes = discovery_service.getNodes()
		# Update Bandwidth Measurments
		nodes = bandwidth_server.update_nodes(nodes)
		# update the OutputmManager
		output_manger.setNodes(nodes)

		time.sleep(1)

def setup():
	global output_manger
	global discovery_service
	global bandwidth_server
	log("Setup Starting")

	# Capture exit signals and run cleanup
	for sig in (signal.SIGABRT, signal.SIGILL, signal.SIGINT, signal.SIGSEGV, signal.SIGTERM):
		signal.signal(sig, cleanup)

	# Generate ID
	Id = uuid.uuid4()
	log("UUID generated: " + str(Id), level=0)

	# Start Bandwidth Server
	bandwidth_server = BandwidthServer(BASE_PORT)
	bandwidth_server.daemon = True
	bandwidth_server.start()
	threads.append(bandwidth_server)

	while not bandwidth_server.is_started():
		time.sleep(0.1)
	bandwidth_port = bandwidth_server.get_port()

	# Start Descovery Service
	discovery_service = DiscoveryService(Id, bandwidth_port, DISCOVERY_PORT)
	discovery_service.daemon = True
	discovery_service.start()
	threads.append(discovery_service)

	# Start Output Manager
	output_manger = OutputManager()
	output_manger.daemon = True
	output_manger.start()
	threads.append(output_manger)

	

def cleanup(signal, frame):
	log("Shutting down Communication Node...", level=0)
	for t in threads:
		t.stop()
	t.join(5)
	sys.exit(0)


if __name__ == "__main__":
	log("Setting up Communication Node...", level=0)
	setup()
	log("Starting Communication Node...", level=0)
	loop()
