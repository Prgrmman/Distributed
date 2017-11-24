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
        - _name: (string) name of replica connected to
        - _active: (bool) True if connection is up and running
        - client: KeyValueStore.Client
        - _hints: (list of Value) a list of hints stored to be sent when the connection
            can become active again
    """
    def __init__(self, ip, port, name):
        self._name = name
        self._hints = []
        self._isActive = False

        transport = TSocket.TSocket(ip, port)
        transport = TTransport.TBufferedTransport(transport)
        self._transport = transport
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self.client = KeyValueStore.Client(protocol)
        self._lock = threading.Lock()


    # returns true if the transport is open 
    def is_active(self):
        return self._active

    # try to (re)open the connection
    def open(self):
        try:
            self._transport.open()
            self._active = True
        except:
            self._active = False

    # close underlying transport
    def close(self):
        self._transport.close()
        self.mark_closed()

    # sets the connection as not being used
    def mark_closed(self):
        self._active = False

    # used to lock around an entire connection object
    def lock(self):
        self._lock.aquire()
    def unlock(self):
        self._lock.release()
    
    # send out everything from _hints
    def send_hints(self):
        pass

    def __eq__(self, other):
       return self._name == other._name

# creates a connection object from a node
def connection_from_node(node):
    return Connection(node.ip, node.port, node.name)

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
