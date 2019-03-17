#!/usr/bin/env python3
import socket
import os
import sys

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
        self.get_args(self.args)

    def get_args(self,line_args):
        #mytmp_list = []
        try:
            index = line_args.index('--host')
            self.ip = line_args[index+1]
        except ValueError:
            print("args --host error!")
            exit(-1)

        #mytmp_list.append(self.config_file)
        try:
            index = line_args.index('--port')
            self.ports = []
            self.ports.append(int(line_args[index+1]))

        except ValueError:
            print("args --port error!")
            exit(-2)
        return None

def scan(host,ports):
    #s = socket.socket()
    #s.settimeout(0.1)  
    #pass
    HOST = host
    PORTS = ports
    print("ports={}".format(ports))
    s = None
    for res in socket.getaddrinfo(HOST,PORTS,socket.AF_UNSPEC,socket.SOCK_STREAM):
        af,socktype,proto,canonname,sa = res
        try:
            s = socket.socket(af,socktype,proto)
            s.settimeout(0.1)  
        except OSError as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        #print('could not open socket')
        print('port {} closed'.format(PORTS))
        sys.exit(1)
    else:
        print('port {} open'.format(PORTS))
    return None


# ------------------------
if __name__ == '__main__':
    if len(sys.argv) <= 1 :
        print("Usage:{} --host x.x.x.x --port single or range[20-25]".format(sys.argv[0]))
    else:
        chuli_args = Args()
        print(chuli_args.ip)
        print(chuli_args.ports[0])
        scan(chuli_args.ip,chuli_args.ports[0])

        
        #scan(host,port)
