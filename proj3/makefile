# Just a quick makefile to build Protocol buffer code
.PHONY: protocol_buff clean

all: protocol_buff


protocol_buff: bank.proto
	protoc --python_out=. bank.proto

clean:
	rm -f *.pyc
	rm -r bank_pb2.py
