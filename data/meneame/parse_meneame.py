#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2016 Carlos Segura. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================


import os
import sys
import gzip

parents = {}

conversations = []

samples = {}

class Sample:
  comentario_id = None
  parent_id = []
  commentario = ''

comentario_id = None
parent_id = []

with gzip.open(sys.argv[1]) as f:
    for line in f:
        try:
            line = line.decode('utf-8').strip()
            #print(line)
            splitted_line = line.split()
            if len(splitted_line) == 0:
                continue
            head = splitted_line[0]
            rest = splitted_line[1:]
            
            if head == 'comentario_id:':
                comentario_id = rest[0]
                parent_id = []
            if head == 'parent_id:':
                parent_id.append(rest[0])
            if head == 'comentario:':
                comentario = rest
                if len(comentario) == 0:
                    comentario_id = None
                    parent_id = []
                    continue

                #Store this comment in parents dictionary
                if comentario_id is not None:
                    sample = Sample()
                    sample.comentario_id = comentario_id
                    sample.parent_id = parent_id
                    sample.comentario = comentario
                    samples[comentario_id] = sample


                comentario_id = None
                parent_id = []
        except:
            continue

for k in samples:
    sample = samples[k]
    for parent in sample.parent_id:
        if parent in samples:
            qa = [samples[parent].comentario, sample.comentario]
            conversations.append(qa)
        
        
for conversation in conversations:
    print('********************************************')
    for frase in conversation:
        print(*frase)
        

        
