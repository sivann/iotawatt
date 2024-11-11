# https://docs.iotawatt.com/en/master/query.html
import requests
import json
import os
import sys

SERIES_FN="series.json"

def get_series(series_fn):
    if not os.path.isfile(series_fn) or os.path.getsize(series_fn)<10:
        print(f"{series_fn} not found or too small, retrieving series from device")
        series = requests.get('http://192.168.123.229/query?show=series')
        st = series.text
        if len(series.text):
            with open(series_fn, 'w') as f:
                f.write(series.text)
        print(f"Done")
    else:
        with open(series_fn, 'r') as f:
            st = f.read()
    stj=json.loads(st)
    return stj


#series_j = get_series(SERIES_FN)
#print(json.dumps(series_j,indent=2))

# [root@greenflame ~/iotawatt]$ curl -g   'http://192.168.123.229/query?select=[R.watts,S.watts,T.watts,R.va,S.va,T.va,R.var,S.var,T.var,R.volts,S.volts,T.volts,R.wh,S.wh,T.wh,R.pf,S.pf,T.pf,Heater.watts,Heater.wh,totpower,Input_0]&begin=s-1h&end=s&group=5m&format=json&header=yes' |jq . > o.json

# Just get series from here:
series = ['R.watts','S.watts','T.watts','R.va','S.va','T.va','R.var','S.var','T.var','R.volts','S.volts','T.volts','R.wh','S.wh','T.wh','R.pf','S.pf','T.pf','Heater.watts','Heater.wh','totpower','Input_0']

param_series=",".join(series)
params={
    'select':f"[{param_series}]",
    'begin':f"s-1h",
    'end':f"s",
    'group':f"5m",
    'header':f"yes",
    }
d = requests.get('http://192.168.123.229/query',params=params)

print(d.text)
