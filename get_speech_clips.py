# identifies all MAN, FAN, and overlap (FAN-OLN-CHN or CHN-OLN-FAN)
# from LENA .its file 
# with basic acoustics and timestamps
# and spits out .csvs
# into speaker-specific directories
# filename and segment type (MAN, FAN, or OLN) must be specified in command line

import re
import sys
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
import random
import pandas as pd
import datetime
from lxml import etree
import numpy as np

#_______________________________________________________________________________


def extract_time(text):
    # removes PT and S from timestamp string and converts it to float
    return float(text[2:-1])

def find_all_speech(its_file):
    utt = []
    # parse as xml file
    xmldoc = etree.parse(its_file)
    # select all nodes that are segments
    seg_id = 0
    for seg in xmldoc.iter('Segment'):
    # print(str(seg))
        if (seg.attrib['spkr']==segment):

            if segment=='FAN':
                wordCount = seg.attrib['femaleAdultWordCnt']
                nonSpeechDur = seg.attrib['femaleAdultNonSpeechLen']
                uttCnt = seg.attrib['femaleAdultUttCnt']
                uttLength = seg.attrib['femaleAdultUttLen']
            elif segment=='MAN':
                wordCount = seg.attrib['maleAdultWordCnt']
                nonSpeechDur = seg.attrib['maleAdultNonSpeechLen']
                uttCnt = seg.attrib['maleAdultUttCnt']
                uttLength = seg.attrib['maleAdultUttLen']
            else:
                wordCount = 'NA'
                nonSpeechDur = 'NA'
                uttCnt = 'NA'
                uttLength = 'NA'

            if (segment=='OLN' or segment=='OLF') and (extract_time(seg.attrib['endTime'])-extract_time(seg.attrib['startTime'])) > 10:
                onset = extract_time(seg.attrib['startTime'])
                offset = extract_time(seg.attrib['endTime'])
                duration = offset-onset
                num_clips = list(range(int(duration)//3)) # number of clips within the larger clip
                for n in num_clips:
                    new_onset = n*3 + onset
                    new_offset = new_onset + 3
                    if n == num_clips[-1]: # for the last clip
                        new_offset = offset
                    else: 
                        new_offset = new_onset + 3 
                    new_duration = new_offset - new_onset
                    avg_dB = seg.attrib['average_dB']
                    peak_dB = seg.attrib['peak_dB']
                    file_name = '{}_{}_{}_{}.wav'.format(int(new_onset), int(new_offset), segment, child_id)
                    seg_id += 1
       
                    utt.append([seg_id, new_onset, new_offset, new_duration, avg_dB, peak_dB, file_name])

            else:
                onset = extract_time(seg.attrib['startTime'])
                offset = extract_time(seg.attrib['endTime'])
                duration = offset - onset
                avg_dB = seg.attrib['average_dB']
                peak_dB = seg.attrib['peak_dB']
                file_name = '{}_{}_{}_{}.wav'.format(int(onset), int(offset), segment, child_id)
                seg_id += 1

                utt.append([seg_id, onset, offset, duration, avg_dB, peak_dB, wordCount, nonSpeechDur, uttCnt, uttLength, file_name])

           
    return utt

#_______________________________________________________________________________

def list_to_csv(list_ts, output_file_name): # to remember intermediaries
    list_ts.to_csv(working_dir+"/"+child_id+'_speech_output/'+output_file_name) # write dataframe to file
#_______________________________________________________________________________

def process_one_file(its):

    all_timestamps = []
    all_timestamps += find_all_speech(its)

    df2 = pd.DataFrame(all_timestamps, columns=["seg_id", "onset", "offset", "duration", "avg_dB", "peak_dB", "wordCount", "nonSpeechDur", "uttCnt", "uttLength", "file_name"]) # df of timestamps
    df2['offset'] = pd.to_numeric(df2['offset']) 
    df2['seconds'] = ((df2['offset'] // 60)*60)+60  # create a column of 'seconds'
    df2['child'] = child_id
    df2['segment_type'] = segment
    df2['random_idx'] = np.random.choice(range(len(df2)), len(df2), replace=False)

    df2.columns = ["seg_id",'clip_onset', 'clip_offset', "duration", "avg_dB", "peak_dB", "wordCount", "nonSpeechDur", "uttCnt", "uttLength", "file_name", "seconds", "child_id", "segment_type", "random_idx"]

    list_to_csv(df2, child_id+"_"+segment+"_"+"timestamps.csv")

#_______________________________________________________________________________

if __name__ == "__main__":


    working_dir = __file__
    working_dir = working_dir[0:working_dir.rfind('/')] # find the last slash in filepath and cut off after that 
    # to run one child at a time 
    filename = sys.argv[1]
    segment = sys.argv[2] # FAN, MAN, OLN, or OLF
    child_id = filename[0:7]
    its_file = working_dir+"/"+filename+'.its' 
    output_dir = working_dir+"/"+child_id+'_speech_output/' # path to the output directory
    if os.path.exists(its_file): 
        if not os.path.exists(output_dir):
            os.mkdir(output_dir) # creating the output directory if it does not exist
    process_one_file(its_file)

  # otherwise to batch process
    segment = sys.argv[1] # FAN, MAN, OLN, or OLF
    
    processed_files = []
    its_files = []
    for f in sorted(os.listdir(working_dir)):
        if f.endswith(".its") and f not in processed_files:
            child_id = f[0:7]
            metadata_df = working_dir+"/"+child_id+'_speech_output/'+child_id+'_'+segment+'_timestamps.csv'
            if not os.path.exists(metadata_df): # if there isn't a metadata sheet for this recording*segment, process the recording; else skip
            filename = f[0:f.rfind('.')] # everything before the extension
            its_file = working_dir+"/"+filename+'.its' 
            output_dir = working_dir+"/"+child_id+'_speech_output/' # path to the output directory
            if os.path.exists(its_file): 
                if not os.path.exists(output_dir):
                    os.mkdir(output_dir) # creating the output directory if it does not exist
                 
                if f[-6]=='_':         # if there are several files from the same day; this code will currently not work for audio
                    its_files = [its_file]
                    for filename_other in os.listdir(working_dir):
                         if filename_other.endswith('.its') and f[:-6]==filename_other[:-6] and f[-5]!=filename_other[-5]:
                             its_files.append(working_dir+"/"+filename_other)
                    process_one_file(its_files)
                for file in its_files:
                    print('processing', file)
                    processed_files.append(file) # append to list after processing
                else:
                     print('processing', f)
                     process_one_file(its_file)
                     processed_files.append(f) # append to list after processing
            else:
                print('already processed',segment,'clips for', child_id)