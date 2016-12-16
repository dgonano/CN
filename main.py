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

def log(log):
	if debug:
		print(log)

def loop():
	while True:
		log("Loop Starting")
		time.sleep(1)


def setup():
	log("Setup Starting")
	# Capture exit signals and run cleanup
	for sig in (signal.SIGABRT, signal.SIGILL, signal.SIGINT, signal.SIGSEGV, signal.SIGTERM):
		signal.signal(sig, cleanup)

def cleanup(signal, frame):
	log("Cleanup Starting")
	sys.exit(0)


if __name__ == "__main__":
	print("Setting up Communication Node...")
	setup()
	print("Starting Communication Node...")
	loop()
