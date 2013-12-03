#!/usr/bin/env python

from ConfigParser import ConfigParser
import helper
import time

def check_server(server):
 (t_width, nill) = helper.getTerminalSize()
 server = dict(server)
 name = server["name"]
 ip = server["ip"]
 port = server["port"]
 path = server["path"]
 protocal = server["protocal"]

 start = "server \033[1m%s \033[0m" %(name)
 end = '\033[92m' + "[OK]" + '\033[0m'
 errorend = "\033[91m[Error]\033[0m"
 space_len = t_width - len(start) - len(end)
 error_space_len = t_width - len(start) - len(end)
 
 if protocal == "http":
  import httplib
  try:
   conn = httplib.HTTPConnection("%s" % (ip), port)
   conn.request("GET" ,path)
   resp = conn.getresponse()
   if str(resp.status) == "200":
    print start, " "* space_len, end
   else:
    helper.notify(name + " (IP: "+ip+") is down !!!")
    print start, " "* error_space_len, errorend
  except Exception, e:
      helper.notify(name + " (IP: " + ip + ") is down !!!")
      print start, " "* error_space_len, errorend

config = ConfigParser()

if __name__ == "__main__":
   while True:
      # Load config file
      config.read("./config.ini")

      # Get config
      checktoday_config = dict(config.items("checktoday"))

      # Check server one by one
      for section in config.sections():
        if section != "checktoday":
          check_server(config.items(section))

      # Redo again after 1min
      time.sleep(checktoday_config["internal"])

