#!/usr/bin/env python

from threading import Thread
import subprocess
from Queue import Queue
import re
import os
import sys
import platform

num_threads = 10
queue = Queue()

def pinger(i,q):
    while True:
        ip = q.get()
        if platform.system() == "Linux":
            cmd = "ping -c 1 %s" % ip

            outfile = "/dev/null"
        elif platform.system() == "Windows":
            cmd = "ping -n 3 %s" % ip
            #outfile = "ping.txt"

        # ret = subprocess.call(cmd, shell=True, stdout=open(outfile,'wb+'), stderr=subprocess.STDOUT)
        ping = os.popen(cmd)
        f = open("ping.txt",'a+')
        f.write(ping.read())
        f.closed

        #if ret == 0:
        #    print "%s: is alive" % ip
        #else:
        #    print "%s is down" % ip
        q.task_done()

for i in range(num_threads):
    worker = Thread(target=pinger, args=(i, queue))
    #worker.setDaemon(True)
    worker.start()


host_file = open(r'hosts.txt','r')
ips = []
re_obj = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
for line in host_file:
    for match in re_obj.findall(line):
        ips.append(match)
host_file.close()
print ips

for ip in ips:
    queue.put(ip)
print "Main Thread Waiting"
queue.join()
print "Done"

result = raw_input("Please press any key to exit")
if result:
    sys.exit(0)