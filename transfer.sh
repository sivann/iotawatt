#!/bin/bash

# Run every hour via cron

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

PATH=$SCRIPT_DIR:$PATH
# Read data from iotawatt, save to output.txt
iolog2zbx.py --begin 's-1h' --period 1

# Then, send to zabbix:
zabbix_sender --input-file zbx-output.txt --with-timestamps -z services.easykenak.gr

