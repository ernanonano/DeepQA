#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

old_speaker = None
new_line = True

with open(sys.argv[1]) as f:
    content = f.readlines()
    for line in content:
        [id, beg, end, word, conf] = line.strip().split()
        [nada, speaker ] = id.split('_')
        
        
        if word == '<garbage>':
            continue
        
        if speaker == 'a':
            speaker = 'AGENT'
        else:
            speaker = 'CLIENT'
        
        if speaker != old_speaker:
            old_speaker = speaker
            new_line = True
        else:
            new_line = False
            
        if new_line:
            print(' .')
            print(speaker + ':', end="")

        #if word != '<garbage>':
        print(' ' + word, end="")
            

print("")    
    
