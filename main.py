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

# Get arguments
parser = optparse.OptionParser()
# parser.add_option('-s', '--silent',
# 		dest="silent",
# 		action="store_true",
# 		default=False,
# 		help="don't display any messages")
parser.add_option('-d', '--debug',
		dest="debug",
		action="store_true",
		default=False,
		help="display debug messages")

cmdopts, cmdargs = parser.parse_args()
# silent = cmdopts.silent
debug = cmdopts.debug

# constants
BASE_PORT = 41000
DISCOVERY_PORT = 42000

# global variables
Id = ''
nodes = []
threads = []

def log(log, level=1):
	if level == 0 or debug:
		print(time.asctime() + "    " + log)

def loop():
	while True:
		log("Loop Starting")

		nodes.append(Node(uuid.uuid4(), "192.168.0.1"))
		nodes.append(Node(uuid.uuid4(), "192.168.0.2"))
		nodes.append(Node(uuid.uuid4(), "192.168.0.3"))
		nodes.append(Node(uuid.uuid4(), "192.168.0.4"))
		nodes.append(Node(uuid.uuid4(), "192.168.0.5"))

		output_manger.set_nodes(nodes)

		time.sleep(15)

def setup():
	global output_manger
	log("Setup Starting")

	# Capture exit signals and run cleanup
	for sig in (signal.SIGABRT, signal.SIGILL, signal.SIGINT, signal.SIGSEGV, signal.SIGTERM):
		signal.signal(sig, cleanup)

	# Generate ID
	Id = uuid.uuid4()
	log("UUID generated: " + str(Id))

	# Start Output Manager
	output_manger = OutputManager()
	output_manger.start()
	threads.append(output_manger)

def cleanup(signal, frame):
	log("Cleanup Starting")
	for t in threads:
		t.stop()
	sys.exit(0)


if __name__ == "__main__":
	log("Setting up Communication Node...", level=0)
	setup()
	log("Starting Communication Node...", level=0)
	loop()
