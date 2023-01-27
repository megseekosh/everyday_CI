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
    # removes PT and S from timestamp string and converts it to float
    return float(text[2:-1])

def find_all_chn(its_file, id="CHN"):
    chi_utt = []
    # parse as xml file
    xmldoc = etree.parse(its_file)
    seg_id = 0
    # select all nodes that are segments
    for seg in xmldoc.iter('Segment'):
        if (seg.attrib['spkr']==id):
            # if segment spoken by CHN, retrieve the onset and offset of utterance
            # .attrib to get attribute from CHN node
            onset = extract_time(seg.attrib['startTime'])
            offset = extract_time(seg.attrib['endTime'])
            duration = offset - onset
            avg_dB = seg.attrib['average_dB']
            peak_dB = seg.attrib['peak_dB']
            childUttCnt = seg.attrib['childUttCnt']
            childUttLen = seg.attrib['childUttLen']
            childCryVfxLen = seg.attrib['childCryVfxLen']
            its_file_name = its_file[its_file.rfind('/')+1:its_file.rfind('.')]            
            seg_id += 1
            
            chi_utt.append([seg_id, onset, offset, duration, avg_dB, peak_dB, childUttCnt, childUttLen, childCryVfxLen, its_file_name])
    
    return chi_utt
#_______________________________________________________________________________


def list_to_csv(list_ts, output_file): # to remember intermediaries
    list_ts.to_csv(working_dir+"/"+child_id+'_voc_output/'+output_file) # write dataframe to file
#_______________________________________________________________________________

def process_one_file(its_file):

    all_chn_timestamps = []
    all_chn_timestamps += find_all_chn(its_file) # get child timestamps


    df2 = pd.DataFrame(all_chn_timestamps, columns=["seg_id", "onset", "offset", "duration", "avg_dB", "peak_dB", "childUttCnt", "childUttLen", "childCryVfxLen", "its_file_name"]) # df of timestamps
    df2['offset'] = pd.to_numeric(df2['offset']) 
    df2['seconds'] = ((df2['offset'] // 60)*60)+60  # create a column of 'seconds'
    df2['segment_type'] = 'CHN'

    df2.columns = ["seg_id", "onset", "offset", "duration", "avg_dB", "peak_dB", "childUttCnt", "childUttLen", "childCryVfxLen", "its_file_name", "seconds", "segment_type"]

    list_to_csv(df2, child_id+"_"+"CHN_timestamps.csv")

#_______________________________________________________________________________

if __name__ == "__main__":

    working_dir = __file__
    working_dir = working_dir[0:working_dir.rfind('/')] # find the last slash in filepath and cut off after that 
    
    # to run one child at a time
    filename = sys.argv[1]
    child_id = filename[0:7]
    output_dir = working_dir+"/"+child_id+'_voc_output/' # path to the output directory
    its_file = working_dir+"/"+filename+'.its' 
    os.mkdir(output_dir) # creating the output directory if it does not exist
    process_one_file(its_file)

    # to batch process
  
     processed_files = []
     for f in sorted(os.listdir(working_dir)):
         if f.endswith(".its") and sum([1 if i[i.rfind("/")+1:] == f else 0 for i in processed_files]) == 0:
             child_id = f[0:7]
             metadata_df = working_dir+"/"+child_id+'_voc_output/'+child_id+'_CHN_timestamps.csv'
             if not os.path.exists(metadata_df): # if there isn't a metadata sheet for this recording*segment, process the recording; else skip
                 filename = f[0:f.rfind('.')] # everything before the extension
                 its_file = working_dir+"/"+filename+'.its' 
                 output_dir = working_dir+"/"+child_id+'_voc_output/' # path to the output directory
                 if os.path.exists(its_file): 
                     if not os.path.exists(output_dir):
                         os.mkdir(output_dir) # creating the output directory if it does not exist

                     print('processing', f)
                     process_one_file(its_file)
                     processed_files.append(f) # append to list after processing
             else:
                 print('already processed CHN clips for', child_id)