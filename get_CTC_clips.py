import re
import sys
import os
from pydub import AudioSegment
import random
import pandas as pd
import datetime
from lxml import etree
import numpy as np

def load_audio(audio):
    init = datetime.datetime.now()
    print("loading audio")
    fullAudio = AudioSegment.from_wav(audio)
    print("audio loaded in ", datetime.datetime.now()-init, " min.sec.ms")
    return fullAudio
#_______________________________________________________________________________


def extract_time(text):
    # removes PT and S characters that surround timestamp strings and converts them to float
    return float(text[2:-1])

def find_all_ct(its_file):
    ct_cnt = [] # count the chunks with <0 turns
    # parse as xml file
    xmldoc = etree.parse(its_file)
    # select all nodes that are segments - I need something else besides segment 
    for seg in xmldoc.iter('Conversation'):
        if (seg.attrib['turnTaking']!='0'):
            # if the # of turns is >0, retrieve the onset and offset of the utterance containing those turns
            # .attrib to get attribute from turnTaking node
            onset = extract_time(seg.attrib['startTime'])
            offset = extract_time(seg.attrib['endTime'])
            avg_dB = seg.attrib['average_dB']
            peak_dB = seg.attrib['peak_dB']
            cnt = seg.attrib['turnTaking'] # get the # of convo turns
            ct_cnt.append([onset, offset, cnt, avg_dB, peak_dB])
    return ct_cnt

#_______________________________________________________________________________

def list_to_csv(list_ts, output_file): # to remember intermediaries
    list_ts.to_csv(working_dir+"/"+child_id+"_CTC_output/"+output_file) # write dataframe to file
#_______________________________________________________________________________

def process_one_file(its):

    all_ct_timestamps = []
    all_ct_timestamps += find_all_ct(its) # get child timestamps
  
    n=1
    seconds = 60
    offset_df = []
    df2 = pd.DataFrame(all_ct_timestamps, columns=["onset", "offset", "convo_count", "avg_dB", "peak_dB"]) # df of timestamps
    df2['duration'] = df2['offset'] - df2['onset'] # find duration of Conversation element
    df2['segment_type'] = 'CTC'
    df2['seconds'] = ((df2['offset'] // 60)*60)+60  # create a column of 'seconds'
    df2['child_id'] = child_id

    df2 = pd.DataFrame(df2)
    df2.columns = ['clip_onset', 'clip_offset', 'convo_count', "avg_dB", "peak_dB", 'duration', 'segment_type', 'seconds', 'child_id']

    list_to_csv(df2,child_id+"_"+"CTC_timestamps.csv")


#_______________________________________________________________________________

if __name__ == "__main__":

    working_dir = __file__
    working_dir = working_dir[0:working_dir.rfind('/')] # find the last slash in filepath and cut off after that 
    
    # to run one child at a time
    filename = sys.argv[1]
    child_id = filename[0:7]
    output_dir = working_dir+"/"+child_id+'_ctc_output/' # path to the output directory
    its_file = working_dir+"/"+filename+'.its' 
    if os.path.exists(its_file): 
        if not os.path.exists(output_dir):
            os.mkdir(output_dir) # creating the output directory if it does not exist
    process_one_file(its_file)

    # otherwise to batch process
  
    processed_files = []
     for f in sorted(os.listdir(working_dir)):
         if f.endswith(".its") and f not in processed_files:
             print(f)
             filename = f[0:f.rfind('.')] # everything before the extension
             its_file = working_dir+"/"+filename+'.its' 
             child_id = f[0:7]
             process_one_file(its_file) # process one child at a time
             processed_files.append(filename) # append to list after processing

         #if there are several files from the same day
         if filename[-6]=='_':
             for filename_other in os.listdir(working_dir):
                  if filename_other.endswith('.its') and filename[:-6]==filename_other[:-6] and filename[-5]!=filename_other[-5]:
                      its_files.append(working_dir+"/"+filename_other)
                      processed_files.append(filename_other)
    process_one_file(its_file)