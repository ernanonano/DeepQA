#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import gzip

prev_sentence=None
ts_start = 0.0
ts_end = 0.0

with gzip.open(sys.argv[1]) as f:
    for line in f:
        #try:
        line = line.decode('utf-8').strip()

        if line.startswith('<'):
            if line.startswith('<time'):
                t = line.split()
                t_id = t[1].split('=')[1].strip("\"")
                t_ts = t[2].split('=')[1].strip("\"")
                t_ts_s = t_ts.replace(',','.').split(':')
                ts = int(t_ts_s[0])*3600+int(t_ts_s[1])*60+float(t_ts_s[2])
                if t_id[-1] == 'S':
                    ts_start = ts
                    if (ts_start > ts_end + 2.0 ):
                        prev_sentence = None
                else:
                    ts_end = ts
        else:
            line = line.replace('-', ' ').strip()
            if prev_sentence is not None:
                if prev_sentence != line and not line.lower().startswith('hola') and not line.lower().startswith('adi') and not line.lower().startswith('hasta')  and len(line) > 1 :
                    print("**************************")
                    print(prev_sentence)
                    print(line)
                
            prev_sentence = line


