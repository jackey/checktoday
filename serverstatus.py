#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import os
import sys
import traceback
import helper
from ConfigParser import ConfigParser
import time

pwd = os.path.dirname(os.path.abspath(__file__))

def check_server_with_ssh(sshhost, sshuser, sshport=21, name=""):
    global info
    paramiko.util.log_to_file(pwd + "/ssh_log")

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(sshhost, sshport, sshuser)
        chan = client.get_transport().open_session()

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

        info += "\n<b>Server: %s </b>\n" % (name)
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
    except Exception, e:
        print "*** Caught exception : %s %s" % (e.__class__, e)

        traceback.print_exc()
        try:
            client.close()
        except:
            pass

if __name__ == "__main__":
    while True:
        info = ""
        config = ConfigParser()
        config.read(pwd + "/config.ini")
        checktoday_config = dict(config.items('checktoday'))

        for section in config.sections():
            if section != "checktoday":
                distance = dict(config.items(section))
                if distance["protocal"] == "ssh":
                    check_server_with_ssh(distance["ip"], distance["user"], distance["port"], distance["name"])

        helper.info(info)
        time.sleep(float(checktoday_config["internal"]))
