#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import os
import sys
import traceback
import socket
import select
import helper

pwd = os.path.dirname(os.path.abspath(__file__))

sshhost = "222.73.219.19"
sshport = "20110"
sshuser = "root"

paramiko.util.log_to_file(pwd + "/ssh_log")

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "*** connecting ..."
    client.connect(sshhost, sshport, sshuser)
    chan = client.get_transport().open_session()

    info = ""

    # Total memory
    chan.exec_command("""cat /proc/meminfo""")
    key = True
    mem_free = 0
    mem_total = 0
    while key:
        if key == chan.recv_ready():
            out = "%s" % (chan.recv(1024 * 100).decode("utf-8"))
            lines = out.split("\n")[:-1]
            for line in lines:
                k, v = line.split(":")
                if str(k).strip() == "MemTotal":
                    mem_total = int(str(v).replace("kB", "").strip())

                if str(k).strip() == "MemFree":
                    mem_free += int(str(v).replace("kB", "").strip())
                if str(k).strip() == "Buffers":
                    mem_free += int(str(v).replace("kB", "").strip())
            break

    info += "\nServer: %s \n" % (sshhost)
    info += "Memfree: %s \n" %( helper.convertSize(mem_free))
    info += "Memtotal: %s\n" %(helper.convertSize(mem_total))

    # num of httpd
    chan = client.get_transport().open_session()
    chan.exec_command("""ps aux | grep httpd | grep -v "grep" | wc -l""")
    num_httpd = 0
    key = True
    while key:
        if chan.recv_ready():
            out = "%s" % (chan.recv(1024 * 100)).decode("ascii")
            info += "number of httpd process: %d"  %(int(out))
            break

    chan.close()
    client.close()
    helper.info(info)
except Exception, e:
    print "*** Caught exception : %s %s" % (e.__class__, e)

    traceback.print_exc()
    try:
        client.close()
    except:
        pass

sys.exit(0)

