'''
This file is for functions that need to be shared between clients and servers
'''
import sys

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
