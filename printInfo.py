#!/usr/bin/env python3
#coding=utf-8

import os
import sys
from FlvMuxer import *

if __name__ == '__main__':
    muxer = FlvMuxer()
    if len(sys.argv) < 2:
        print('Please specify the input file')
        print('Usage: ./printInfo.py input.flv [video|audio|meta|all(default)|brief]')
        exit()
    if len(sys.argv) > 2:
        if sys.argv[2] == 'all' or sys.argv[2] == 'brief':
            target_type = sys.argv[2]
        elif sys.argv[2] not in type_code:
            print('Invalid type specified')
            exit()
        else:
            target_code = type_code[sys.argv[2]]
    else:
        target_type = 'all'

    muxer.open_input_file(sys.argv[1])
    l = muxer.get_tag_list()
    print('Video:    ', muxer.video_info)
    print('Audio:    ', muxer.audio_info)
    print('Duration: ', muxer.duration / 1000.0, 'sec')
    if target_type == 'brief':
        exit()
    for tag in l:
        if target_type == 'all' or tag.type == target_code:
            print('No: ', tag.index, ', type: ', tag.type, ', timestamp: ', tag.timestamp, ', size: ', tag.size, ', detail: ', tag.data_info)

