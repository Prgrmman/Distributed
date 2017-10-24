#!/usr/bin/env python

import sys
sys.path.append('/home/phao3/protobuf/protobuf-3.4.0/python')
import bank_pb2 as bank
import os
import struct
import socket

###GLOBALS

HEADER_SIZE = 4

'''
This is a module provides a front end for sending google protobuf
    messages over sockets
'''

# header length is 4 bytes
# the message should be of a BranchMessage type
def send__message(socket, msg):
    """ socket: (Socket)
        msg: some Google protobuff object
        output: sends data over socket with fixed length header
    """
    assert(type(msg) == bank.BranchMessage)
    msg_text = msg.SerializeToString()
    msg_length = len(msg_text)
    msg_header = struct.pack(">I", msg_length)
    full_msg  = msg_header + msg_text
    socket.sendall(full_msg)


def read_message(socket):
    """ socket: (Socket)
        output: the appropriate bank_pb2 Message object)
    """

    header = socket.recv(HEADER_SIZE)
    msg_length = struct.unpack(">I", header)[0]
    msg_text = socket.recv(msg_length)

    generic_msg = bank.BranchMessage()
    generic_msg.ParseFromString(msg_text)

    msg_field = generic_msg.WhichOneof("branch_message")
    # make sure that at least one of the fields is set
    assert(not msg_field is None)
    msg_object = eval("generic_msg." + msg_field)
    print(msg_object)
    return msg_object


### TEST code

if __name__ == '__main__':
    transfer = bank.Transfer()
    transfer.money = 1

    branch_msg = bank.BranchMessage()
    branch_msg.transfer.CopyFrom(transfer)
    msg_type = branch_msg.WhichOneof("branch_message")

    assert(msg_type == "transfer")
    assert(type(branch_msg.transfer) == bank.Transfer)
    print(eval("branch_msg." + msg_type))
    print("Unit test pass!")
