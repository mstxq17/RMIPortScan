#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import Pyro4, Pyro4.naming
import threading, math

ns = Pyro4.naming.locateNS(host="localhost", port=9091)

def getServers():
    # 获取已经注册的服务
    servers = ns.list()
    okServer = []
    for item in servers.keys():
        if item != 'Pyro.NameServer':
            okServer.append(item)
    return okServer

def getTasks(ports):
    okServer = getServers()
    count = len(okServer)
    return dict(zip(okServer, chunks(ports, count)))


# listTemp 为列表 平分后每份列表的的个数n
def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]

def work(target, service, ports):
    ns = Pyro4.naming.locateNS(host="localhost", port=9091)
    uri = ns.lookup(service)
    scaner = Pyro4.Proxy(uri)
    print(scaner.fastPortScan(target, ports))

def main():
    # 扫描目标111.230.197.23的8000-9000的端口
    target = '111.230.197.23'
    ports = []
    for p in range(8000, 9001):
        ports.append(p)
    tasks = getTasks(ports)
    # 开始扫描
    ns = Pyro4.naming.locateNS(host="localhost", port=9091)
    thread_list = []
    for service,ports in tasks.items():
        thread = threading.Thread(target=work, args=(target, service, ports))
        thread.daemon = True
        thread.start()
        thread_list.append(thread)

    for t in thread_list:
        t.join()
    print("Done!")

if __name__ == '__main__':
    main()