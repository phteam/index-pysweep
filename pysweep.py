#!/usr/bin/env python
# by Index 2014.05.11
# http://asianzines.blogspot.com

import socket, re, os, subprocess
import subprocess
from Queue import Queue
from threading import Thread
from sys import stdout


def pingsweep(i, q):
	while True:
		ipadd = q.get()
		ret = subprocess.call("ping -c 1 -W 2 %s" % ipadd,
		    shell=True,
		    stdout=open('/dev/null', 'w'),
		    stderr=subprocess.STDOUT)
		if ret == 0:
		    print '[+] %s: is online.' % ipadd
		q.task_done()

def main():
	print '\n\t:: [PH] Index Python Ping Sweep ::'
	print '\t  http://asianzines.blogspot.com\n\n'

	print '[-] Attempting to retrieve local address'

	local = ''
	threads = 20
	queue = Queue()
	
	if len(local) == 0:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8", 80))
			local = s.getsockname()[0]
			s.close()
		except: 
			print 'Local address could not be determined.\n'
			exit(0)		

	octet = re.split(r'(\.|/)', local)

	print '[-] Local address determined.\n\n'
	print '[-] Running ping sweep with %d threads' %threads
	print '###### Starting enumeration of %s.%s.%s.x: ######\n' % (octet[0], octet[2], octet[4])

	ips = ['%s.%d' %(''.join(octet[0:-2]), i) for i in range(1,256)]

	for i in range(threads):
	    worker = Thread(target=pingsweep, args=(i, queue))
	    worker.setDaemon(True)
	    worker.start()

	for ip in ips: queue.put(ip)
	queue.join()

	print '\n###### FIN ######\n'

if __name__ == '__main__':
  main()
