#!/usr/bin/env python2

import glob
import sys
import logging
logging.basicConfig(filename = '/dev/null')
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/home/yaoliu/src_code/local/lib/lib/python2.7/site-packages')[0])

from store import KeyValueStore
from store.ttypes import SystemException, Value


from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from util import read_node_file, halt, Node, Connection, connection_from_node
from time import sleep


#Globals
NODE_FILE = ""
connection = None


#Helper functions

#TODO write me
def start_console():
    # Test code please remove
    connection.client.write(Value(0, "hello world", 0.99), 1)
    connection.client.read(0, 1)
    # end test code
    while True:
        command = raw_input(">> ")


# prints out a usage message
def usage(prog_name):
    msg = "Usage: %s node_file " % (prog_name)
    print(msg)
    sys.exit(1)


def main(args):
    global NODE_FILE, connection

    if len(args) != 2:
        usage(args[0])
    NODE_FILE = args[1]

    node_list = read_node_file(NODE_FILE)
    node = node_list[0]

    #TODO Testing code
    connection = connection_from_node(node)
    connection.open()
    if connection.is_open():
        print("We did it")
    else:
        halt("can't connect")
    #TODO end Testing code remove it

    start_console()


###Main
if __name__ == '__main__':
    args = sys.argv
    main(args)

    
