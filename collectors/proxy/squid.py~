import argparse
from urlparse import urlparse
import sys
import db_loader
import re
import time

aid = 'squid_sql'
name = "Squid collector for SQL DBs"
desc = "It parses Squid logs and put them in a DB.\n"
"""
You have to modify the squid config to log the size of the requests:
logformat squid	%ts.%03tu %6tr %>a %Ss/%03>Hs %<st %>st %rm %ru %[un %Sh/%<a %mt
"""

def collect(filename, connector):
    fd = open(filename,'r')
    count_success = 0
    count_fail = 0
    for line in fd:
        line = line.split()
        ts = float(line[0])
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
        duration = line[1]
        ip_src = line[2]
        status = line[3]
        sz_reply = line[4]
        sz_request = line[5]
        method = line[6]
        url = line[7]
        domain = ""
        port = 80
        if url[:7] == "http://":
            domain = url[7:(url[7:].find("/"))+7]
            if domain.find(":")>-1:
                port = domain.split(":")[1]
                domain = domain[0:domain.find(":")]
        else:

            if domain.find("/")>-1:
                domain = url[:url.find("/")]
            else:
                domain = url
            
            if domain.find(":")>-1:
                port = domain.split(":")[1]
                domain = domain[0:domain.find(":")]

        
        user = line[8]
        ip_dst = line[9].split('/')[1]
        obj_type = line[10]

        query = "insert into squid3 (time, duration, ip_src, status, sz_reply, "
        query += "sz_request, method, url, domain, port, user, ip_dst, "
        query += "obj_type) values (\'%s\', %s, \'%s\', \'%s\', %s, %s, \'%s\', \'%s\', \'%s\', %s, \'%s\', \'%s\', \'%s\')" % (ts,
            duration, ip_src, status, sz_reply, sz_request, method, 
            url, domain, port, user, ip_dst, obj_type)

        try:
            db_loader.db_query(connector, query);
            count_success += 1
        except Exception, e:
            print query
            print e
            count_fail += 1

    return count_success, count_fail


def launch(connector):
    filename = "<Path to the log file>"
    suc, fail = collect(filename, connector)
    return suc, fail
