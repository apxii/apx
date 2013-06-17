#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Обновление данных в DNS на Яндексе
'''

import urllib2
import xml.etree.ElementTree as et
import argparse

def YandexGetDomainRecords(token,domain):
    url="https://pddimp.yandex.ru/nsapi/get_domain_records.xml?token=%s&domain=%s" % (token,domain)
    f=urllib2.urlopen(url)
    return f.read()

def YandexEditARecord(token,domain,subdomain,record_id,address):
    url="https://pddimp.yandex.ru/nsapi/edit_a_record.xml?token=%s&domain=%s&subdomain=%s&record_id=%s&content=%s" % (token,domain,subdomain,record_id,address)
    f=urllib2.urlopen(url)

    rt=et.fromstring(f.read())
    err=rt.find('./domains/error')
    errtext=err.text
    if errtext!='ok':
	print "Error updating %s: %s" % (subdomain, errtext)
	return 1

    return 0

def YandexAddARecord(token,domain,subdomain,address):
    url="https://pddimp.yandex.ru/nsapi/add_a_record.xml?token=%s&domain=%s&subdomain=%s&content=%s" % (token,domain,subdomain,address)
    f=urllib2.urlopen(url)

    rt=et.fromstring(f.read())
    err=rt.find('./domains/error')
    errtext=err.text
    if errtext!='ok':
	print "Error adding %s: %s" % (subdomain, errtext)
	return 1

    return 0

def YandexDomainRecordsUpdate(token,domain,rxml,subdomain,address):
    root=et.fromstring(rxml)
    err=root.find('./domains/error')
    errtext=err.text
#    print "Response error is '%s'" % errtext
    if errtext!='ok': return 1

    ret=-1
    for dmn in root.findall("./domains/domain/response/record[@subdomain='%s']" % subdomain):
	if dmn.get("type")=='A':
#	    print dmn.tag,dmn.attrib,dmn.text
#	    print dmn.get("id"), dmn.get("subdomain"), dmn.get("type")
	    record_id=dmn.get("id")
	    if dmn.text!=address:
		ret=YandexEditARecord(token,domain,subdomain,record_id,address)
	    else:
		print "Address of %s is the same (%s), not updating" % (subdomain,address)
		ret=0

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
    rxml=YandexGetDomainRecords(args.token,args.domain)
    #print rxml
    YandexDomainRecordsUpdate(args.token,args.domain,rxml,args.host,args.address)
