#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import Pyro4
import Pyro4.naming
from scapy.all import *
import socket, threading
from queue import Queue

@Pyro4.expose
class Server(object):
    def demoScan(self, target, port):
        return (f"Scaning {target}:{port}")

    # TCP SYN半开扫描, 类似nmap -sS 模式
    def synTcpScan(self, target, port, result=None):
        print(f"{target}:{str(port)}")
        # 扫描端口
        try:
            #构造一个 flag的值为S的报文
            packet = IP(dst=target)/TCP(dport=port, flags='S')
            send = sr1(packet, timeout=2, verbose=0)
            if (send is None):
                if result is not None:
                    result[port] = False
                    return result
                else:
                    return False
            if send.haslayer('TCP'):
                # 判断目标主机是否返回 SYN+ACK
                if send['TCP'].flags == 'SA':
                    sr1(IP(dst=target)/TCP(dport=port,flags='R'),timeout=2,verbose=0)
                    if result is not None:
                        result[port] = True
                        return result
                    else:
                        return True
                elif send['TCP'].flags == 'RA':
                    if result is not None:
                        result[port] = False
                        return result
                    else:
                        return False
        except Exception as e:
            return e

    # 多线程扫描模式
    def fastPortScan(self, target, ports):
        # 默认限制100进程
        thread_limit = 50
        port_queue = Queue()
        result = {}
        thread_list = []
        if not isinstance(ports, list):
            return "ports param is not list!"
        else:
            for p in ports:
                port_queue.put(p)

        while threading.activeCount() < thread_limit and not port_queue.empty():
            port = port_queue.get()
            thread = threading.Thread(target=self.synTcpScan, args=(target, port, result))
            thread_list.append(thread)
            thread.start()
        for t in thread_list:
            t.join()
        return result

def startServer():
    server = Server()
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS(host="localhost", port=9091)
    uri = daemon.register(server)
    ns.register("server", uri)
    print("Ready. Object uri =", uri)
    daemon.requestLoop()


def startNs():
    ns_thread = threading.Thread(
    target=Pyro4.naming.startNSloop, kwargs={'host': "localhost", 'port':9091})
    ns_thread.daemon = True
    ns_thread.start()

def test():
    # server = Server()
    # print(server.fastPortScan("111.230.197.23", [80,90]))
    pass

def main():
    startNs()
    startServer()

if __name__ == '__main__':
    main()
