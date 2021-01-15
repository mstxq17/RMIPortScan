#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import Pyro4, Pyro4.naming

ns = Pyro4.naming.locateNS(host="localhost", port=9091)
uri = ns.lookup("server")
# print(uri)
server = Pyro4.Proxy(uri)
print(server.demoScan("127.0.0.1", "9091"))
print(server.synTcpScan("111.230.197.23", 80))
print(server.fastPortScan("111.230.197.23", [80,90]))