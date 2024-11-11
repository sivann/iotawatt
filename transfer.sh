#!/bin/bash

# Run every hour
# Read data from iotawatt, save to output.txt
iolog2zbx.py --begin 's-1h' --period 1

# Then, send to zabbix:
zabbix_sender --input-file zbx-output.txt --with-timestamps -z services.easykenak.gr

