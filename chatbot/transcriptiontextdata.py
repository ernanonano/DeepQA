#!/usr/bin/env python3

# Copyright 2015 Conchylicultor. All Rights Reserved.
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
# ==============================================================================

"""
Loads the dialogue corpus, builds the vocabulary
"""

import numpy as np
import nltk  # For tokenize
from tqdm import tqdm  # Progress bar
import pickle  # Saving the data
import math  # For float comparison
import os  # Checking file existance
import random


from chatbot.basetextdata import BaseTextData



class TranscriptionTextData(BaseTextData):
    """Dataset class
    Warning: No vocabulary limit
    """
    
    def __init__(self, args):
        """Load all conversations
        Args:
            args: parameters of the model
        """
        # Path variables
        self.corpusDir = os.path.join(args.rootDir, 'data/transcriptions/')
        super().__init__(args)
        
    def _loadCorpus(self):
        print('loading corpus')
        transcriptionData = self.loadAndParseTranscriptions(self.corpusDir + 'transcripciones_output_2016_01.txt')
        self.createCorpus(transcriptionData)
    

    def createCorpus(self, conversations):
        """Extract all data from the given vocabulary
        """
        # Add standard tokens
        self.padToken = self.getWordId("<pad>")  # Padding (Warning: first things to add > id=0 !!)
        self.goToken = self.getWordId("<go>")  # Start of sequence
        self.eosToken = self.getWordId("<eos>")  # End of sequence
        self.unknownToken = self.getWordId("<unknown>")  # Word dropped from vocabulary
        
        # Preprocessing data

        for conversation in tqdm(conversations, desc="Extract conversations"):
            self.extractConversation(conversation)

        # The dataset will be saved in the same order it has been extracted

    def extractConversation(self, conversation):
        """Extract the sample lines from the conversations
        Args:
            conversation (Obj): a convesation object containing the lines to extract
        """
            
        # Iterate over all the lines of the conversation
        for i in range(0,len(conversation) - 1, 2):  # We ignore the last line (no answer for it)
            inputLine  = conversation[i]
            targetLine = conversation[i+1]
            
            #print('Conversation ' + str(i) + ' inputLine ' + str(inputLine) + ' targetLine ' + str(targetLine))
            
            inputWords  = self.extractText( " ".join(inputLine) )
            targetWords = self.extractText( " ".join(targetLine), True)
            
            if inputWords and targetWords:  # Filter wrong samples (if one of the list is empty)
                self.trainingSamples.append([inputWords, targetWords])


    def loadAndParseTranscriptions(self, input_file):
        """Loads the transcription file and prepares conversations
        """
        conversations = []
        conversation = []
        with open(input_file) as f:
            is_header = False
            for line in f:
                if line.startswith( 'Processing'):
                    if len(conversation) != 0:
                        conversations.append(conversation)
                        conversation = []
                    continue
                
                if len(line.strip()) == 0:
                    continue

                if line.strip().startswith( '.'):
                    is_header = True
                    continue
                
                if is_header == True:
                    splitted_line = line.strip().split()
                    speaker = splitted_line[0]
                    #print(splitted_line)
                    #Start conversations allways with the client speaking first
                    if speaker != 'CLIENT:':
                        continue
                    is_header = False
                    
                splitted_line = line.strip().split()
                #print(splitted_line)
                speaker = splitted_line[0]
                text = splitted_line[1:]
                conversation.append(text)    
                
        return conversations
                
