#!/usr/bin/env python3

# Read data from iotawatt, save to zbx-output.txt
# After that: zabbix_sender --input-file zbx-output.txt --with-timestamps -z services.easykenak.gr
# Different group minutes needs different zbx item, grouping in different periods will have different results

import os
import sys
import json
import requests
import argparse

parser = argparse.ArgumentParser(description='Query iotawatt, export data for zabbix_sender', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-p','--period', help='Grouping period (minutes)', default=1)
parser.add_argument('-s','--series', help='Series name', default='totpower.wh')
parser.add_argument('-z','--zabbix-host', dest='zabbix_host', help='name of zabbix host', default='greenflame')
parser.add_argument('-i','--output-file', dest='output_file', help='name of zabbix host', default='zbx-output.txt')
parser.add_argument('-b','--begin', dest='begin', help='begin, relative to now, see iotawatt docs', default='s-1h')
parser.add_argument('-e','--end', dest='end', help='end, relative to now, see docs', default='s')
args = vars(parser.parse_args())

print(f"Saving iotawatt response to iw-out.json, converted zabbix data to {args['output_file']}")
print(args)


zbx_host=args['zabbix_host']
group_minutes=args['period']
param_series=args['series']

params={
    'select':f"[{param_series}]",
    'begin':args['begin'],
    'end':args['end'],
    'group':f"{group_minutes}m",
    'header':f"yes",
    'format':f"json",
    }

d = requests.get('http://192.168.123.229/query',params=params)

data = d.text



with open('iw-out.json',"w") as f:
    f.write(data+"\n")


zbxdata=''

#with open(sys.argv[1],"r") as f:
#    data=f.read()

dj=json.loads(data)

begin_ts=dj['range'][0]

li=-1
ts=begin_ts
for label in dj['labels']:
    li+=1
    for row in dj['data']:
        value=row[li]
        #print(label,value)
        x = f"{zbx_host} iotawatt[{label}_wh_{group_minutes}min] {ts} {value}"
        print(x)
        zbxdata+=x+"\n"
        ts = ts + int(group_minutes)*60

with open(args['output_file'],"w") as f:
    f.write(zbxdata)
