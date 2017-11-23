'''
This file is for functions that need to be shared between clients and servers
'''
import sys
import threading
import glob
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/home/yaoliu/src_code/local/lib/lib/python2.7/site-packages')[0])
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from store import KeyValueStore

class Node:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port

    def __str__(self):
        string = "Node \n"
        string += "name: %s\n" %(self.name)
        string += "ip: %s\n" %(self.ip)
        string += "port: %d\n" %(self.port)
        return string


class Connection:
    """
    A Wrapper around a client object
    Attributes:
        - _transport: (TSocket.TSocket)
        - _lock: (threading.Lock)
        - client: KeyValueStore.Client
    """
    def __init__(self, ip, port):
        transport = TSocket.TSocket(ip, port)
        transport = TTransport.TBufferedTransport(transport)
        self._transport = transport
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self.client = KeyValueStore.Client(protocol)
        self._lock = threading.Lock()

    # returns true if the transport is open 
    def is_open(self):
        return self._transport.isOpen()

    # try to (re)open the connection
    def open(self):
        try:
            self._transport.open()
        except:
            pass

    # used to lock around an entire connection object
    def lock(self):
        self._lock.aquire()
    def unlock(self):
        self._lock.release()
def read_node_file(file_name):
    replica_list = []
    with open(file_name) as file:
        for i in range(4):
            line = file.readline().rstrip()
            words = line.split()
            if len(words) != 3:
                raise Exception("Bad file format")
            replica_list.append(Node(words[0], words[1], int(words[2])))
    return replica_list

# halts program with optional message
def halt(msg=None):
    if msg:
        print(msg)
    sys.exit(1)
