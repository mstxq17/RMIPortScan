#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import Pyro4, Pyro4.naming
import threading

def startNs():
    ns_thread = threading.Thread(
    target=Pyro4.naming.startNSloop, kwargs={'host': "localhost", 'port':9091})
    ns_thread.daemon = True
    ns_thread.start()
    ns_thread.join()

if __name__ == '__main__':
    startNs()
