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
from store.ttypes import Value

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
        - client: KeyValueStore.Client
        - _hints: (list of Value) a list of hints stored to be sent when the connection
            can become active again
        - _failed: (bool) true if this connection has failed: used for hinted handoff 
    """
    def __init__(self, ip, port, name):
        self._name = name
        self._hints = []
        self._failed = False

        transport = TSocket.TSocket(ip, port)
        transport = TTransport.TBufferedTransport(transport)
        self._transport = transport
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self.client = KeyValueStore.Client(protocol)
        self._lock = threading.Lock()



    # try to (re)open the connection
    def open(self):
        try:
            self._transport.open()
        except:
            pass

    # close underlying transport
    def close(self):
        self._transport.close()

    # sets the connection as not being used
    def mark_failed(self):
        self._failed = True

    def is_failed(self):
        return self._failed

    # used to lock around an entire connection object
    def lock(self):
        self._lock.acquire()
    def unlock(self):
        self._lock.release()
    

    def add_hint(self, value):
        self._hints.append(value)

    # send out everything from _hints
    def send_hints(self, from_node):
        success = True # assume that this will work

        self.lock()
        self.open()

        for value in self._hints:
            try:
                self.client.put_key(value, from_node)
            except:
                self.mark_failed()
                success = False
                break


        # clear the hints on success
        if success:
            self._hints = [] 
            self._failed = False

        self.close()
        self.unlock()

    def __eq__(self, other):
       return self._name == other._name

# creates a connection object from a node
def connection_from_node(node):
    return Connection(node.ip, node.port, node.name)

# returns an dummy value object
def value_from_string(string):
    return Value(0, string, 0.0)

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
