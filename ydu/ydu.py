#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Обновление данных в DNS на Яндексе
'''

import urllib
import urllib2
import argparse
import json

def YandexGetDomainRecords(token,domain):
    headers = {}
    headers ["PddToken"] = token
    url = "https://pddimp.yandex.ru/api2/admin/dns/list?domain={0}".format(domain)
    req=urllib2.Request(url, headers = headers)
    #print (url)
    #print (req.headers)
    f=urllib2.urlopen(req)

    return f.read()

def YandexEditARecord(token,domain,subdomain,record_id,address):
    headers = {}
    headers ["PddToken"] = token
    url="https://pddimp.yandex.ru/api2/admin/dns/edit"

    values = {}
    values ["domain"] = domain
    values ["record_id"] = record_id
    values ["subdomain"] = subdomain
    values ["content"] = address

    data = urllib.urlencode(values)
    req=urllib2.Request(url, data, headers)

    f=urllib2.urlopen(req)

    rt=json.loads(f.read())
    print(rt)
    errtext=rt["success"]
    if errtext!='ok':
        print ("Error updating %s: %s" % (subdomain, errtext))
        return 1

    return 0

def YandexAddARecord(token,domain,subdomain,address):
    headers = {}
    headers ["PddToken"] = token
    url="https://pddimp.yandex.ru/api2/admin/dns/add"

    values = {}
    values ["domain"] = domain
    values ["type"] = "A"
    values ["subdomain"] = subdomain
    values ["content"] = address

    data = urllib.urlencode(values)
    req=urllib2.Request(url, data, headers)

    f=urllib2.urlopen(req)

    rt=json.loads(f.read())
    print(rt)
    errtext=rt["success"]
    if errtext!='ok':
        print ("Error updating %s: %s" % (subdomain, errtext))
        return 1

    return 0

def YandexDomainRecordsUpdate(token,domain,rt,subdomain,address):
    root=json.loads(rt)
    #print(root)
    errtext=root["success"]
    #print "Response error is '%s'" % errtext
    if errtext!='ok': return 1

    ret=-1
    for dmn in root["records"]:
        if dmn["type"]=='A' and dmn["subdomain"]==subdomain:
            record_id=dmn["record_id"]
            if dmn["content"]!=address:
                ret=YandexEditARecord(token,domain,subdomain,record_id,address)
            else:
                print "Address of %s is the same (%s), not updating" % (subdomain,address)
                ret=0

    return 0
    if ret==-1:
        ret=YandexAddARecord(token,domain,subdomain,address)

    return ret

'''
MAIN
'''

parser=argparse.ArgumentParser(description="Update Yandex DNS")
parser.add_argument("--token",help="Yandex API Token")
parser.add_argument("--domain",help="Domain to update")
parser.add_argument("--host",help="Host")
parser.add_argument("--address",help="Address")

args=parser.parse_args()

if (args.token==None) or (args.domain==None) or (args.host==None) or (args.address==None) :
    parser.print_help()
else:
    rt=YandexGetDomainRecords(args.token,args.domain)
    YandexDomainRecordsUpdate(args.token,args.domain,rt,args.host,args.address)
