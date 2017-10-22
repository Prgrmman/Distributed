#!/usr/bin/python3


'''
This is my http server module.
'''

###Imports

import sys
import os
import socket
from threading import Thread, Lock
from mimetypes import guess_type
import re
from time import strftime, gmtime


###Globals

##Constants

SERVER_NAME = "Ov3rKill"

#The server must run on the specified remote machine
HOST_NAME = "remote.cs.binghamton.edu"

# all requested resources are in the www directory
RES_PATH = "www/" 


NOT_FOUND = """\
HTTP/1.1 404 Not Found


The resource you were looking for could not be located
"""

TIME_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"


###Class definitions

class HTTPServer:
    """ class HTTPServer:

        Attributes:
             _port_number (int): port that the server is listening on
             _server_name (string): name of the server  
             _server_socket (socket): the socket the server listens on
             _resource_count: (dictionary): a dictionary of known resource to the server

        Methods:
            start, get_port_number, get_server_name, __handle_connection, __access_resource
        
    """
    def __init__(self, name=SERVER_NAME):
        self._server_name = name
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._port_number = 0   # default port number (the OS will give us a new one)
        self._resource_count = {}
        self._resource_lock = Lock()
        

    #public methods
    def start(self):
        """ Desc: listen starts up the server on an open port
            input: none
            output: none
        """

        #change path
        if not os.path.exists("www"):
            halt("HTTPServer.start: directory www does not exist")
        os.chdir(RES_PATH)

        #bind the socket to an open port
        try:
            self._server_socket.bind((HOST_NAME, self._port_number))
        except socket.error:
            halt("HTTPServer.start: can't bind socket")

        self._port_number = self._server_socket.getsockname()[1]

        #listen
        try:
            self._server_socket.listen(5) # queue up to 5 requests
        except socket.error:
            halt("HTTPServer.start: can't listen on socket")

        print(" Starting server <{}> with host <{}> and port <{}>".format(
            self._server_name, HOST_NAME , self._port_number))

        #Main server loop
        while True:
            connection, client_address = self._server_socket.accept()

            thread = Thread(target=self.__handle_connection, args=(connection, client_address))
            thread.start()

    def __handle_connection(self, connection, address):
        """ Desc: handle a client connection
            input: connection (socket), address (string)
            output: none
        """
        request = connection.recv(4096) # Hopefully that is enough
        response = ""

        #decode and pare request
        request = request.decode('ascii')
        resource_regex = "GET\s+/([\._\-\w]*)" # get the legal UNIX file name following GET /
        try:
            resource_name = re.match(resource_regex, request).groups()[0]
        except:
            halt("handle_connection: bad HTTP request")

        resource_name = resource_name.strip()

        # Give a report of what just happened to stdout

        resource_found, response = format_response(resource_name)
        if resource_found:
            access_count = self.__access_resource(resource_name)
            server_report = "/{}|{}|{}|{}".format(
                    resource_name, address[0], address[1], access_count)
            print(server_report)
            connection.sendall(response)
            connection.close()
        else:
            connection.sendall(response)
            connection.close()
            halt("Error, resource not found")

    def __access_resource(self, url):
        """ Desc: access a resource and returns how many times it has been accessed
            input: url (string) => the resource in question
            output: (int) => number of times resource has been accessed
        """

        self._resource_lock.acquire()

        self._resource_count[url] = self._resource_count.get(url, 0)
        self._resource_count[url] += 1
        count = self._resource_count[url]

        self._resource_lock.release()

        return count


    def get_port_number(self):
        return self._port_number

    def get_server_name(self):
        return self._server_name


###Internal helper functions


def halt(msg):
    """ prints msg to stderr and exit """
    print(msg, file=sys.stderr)
    os._exit(1)


def format_response(url):
    """ returns a string representing the HTTP response
        input: ()
        output: (status, message)
            - status: a true or false value indicated if the resource was found
            - message: a byte stream to send back to the client
        Note, the url file should exist
    """

    if os.path.isfile(url) == False:
        return (False, NOT_FOUND.encode())

    response = ""
    response += "HTTP/1.1 200 OK\n"
    response += "Date: {}\n".format(rfc_date())
    response += "Server: {}\n".format(SERVER_NAME)
    response += "Last-Modified: {}\n".format(rfc_modified_date(url))
    response += "Content-Length: {}\n".format(os.path.getsize(url))
    response += "Content-Type: {}\n".format(get_mime_type(url))
    response += "Connection: close\n\n"
    
    url_file = open(url, "rb")
    content = url_file.read()
    url_file.close()

    response = response.encode() 
    response += content
    return (True, response)


def get_mime_type(url):
    """ tries to return the MIME type of the url
        input: url(string)
        output: (string or None)
            returns a mime type string if valid mime type, returns None otherwise
    """
    
    mime_type = guess_type(url, strict=True)[0]
    if mime_type == None:
        mime_type = "application/octet-stream"
    return mime_type

def rfc_date():
    """ input: ()
        output: returns a string of the date in RFC 7231 format 
    """

    date_string = strftime(TIME_FORMAT, gmtime())
    return date_string

def rfc_modified_date(url):
    """ input: (url)=> url should refer to a valid file
        output: returns the rfc formatted time when url was modified
    """
    date_string = strftime(TIME_FORMAT, gmtime(os.path.getmtime(url)))
    return date_string



###TESTS

###Execute Main (for tests only)
def TESTS():

    # test get_mime_type
    url = "/docs/test.jpg"
    print("test get_mime_type")
    mime_type = get_mime_type(url)
    assert(mime_type == "image/jpeg")
    print("...pass")


    server = HTTPServer()
    server.start()


if __name__ == "__main__":
    TESTS()
