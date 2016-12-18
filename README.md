# Requirements

The connection Node is built with python 2.7 and requires the following packages, 
- importlib
- os
- time
- sys
- signal
- threading
- requests
- optparse
- uuid
- **pexpect**
- socket 

Non-standard packages are highlighted in **bold**. 

# Compiling, Installation & Running

The program does not require compiling or Installation.

1. Clone the repository to a directory of choice `git clone https://github.com/dgonano/CN.git`
2. To run the Connection Node, `./main.py`

To cleanly shutdown the Node, simple use `ctrl-c`

# Sample Output

For a sample output please see `sampleout.txt` in the main directory. 
This sample was taken with the following setup,
- 2 x Connection Nodes running on a raspberry pi @ 192.168.2.8 (N1 N2)
- 2 x Connection Nodes running on a Macbook pro @ 192.168.2.6 (N3, N4)

The following steps were taken
- N1 was started
- N2 was started 
- N3 was started
- N4 was started
- Left to run for a little while 
- N3 was shutdown
- N4 was shutdown
- N2 was shutdown
- N1 was shutdown

The sample is the output of N1. 