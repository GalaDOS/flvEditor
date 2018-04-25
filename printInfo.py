#!/usr/bin/env python3
#coding=utf-8

import os
import sys
from FlvMuxer import *

def print_info(input_filename, target_type):
    target_code = 0
    if target_type != 'all' and target_type != 'brief':
        if target_type not in type_code:
            print('Invalid type specified')
            return
        else:
            target_code = type_code[target_type]

    code_type = {18:'meta', 8: 'audio', 9: 'video'}
    muxer = FlvMuxer()
    if not muxer.open_input_file(input_filename):
        return
    l = muxer.get_tag_list()
    print('Video:    ', muxer.video_info)
    print('Audio:    ', muxer.audio_info)
    print('Duration: ', muxer.duration / 1000.0, 'sec')
    if target_type == 'brief':
        exit()
    for tag in l:
        if target_type == 'all' or tag.type == target_code:
            if tag.type in code_type:
                type_print = code_type[tag.type]
            else:
                type_print = 'unknown'
            print('No: ', tag.index, ', type: ', type_print, ', timestamp: ', tag.timestamp, ', size: ', tag.size, ', detail: ', tag.data_info)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please specify the input file')
        print('Usage: ./printInfo.py input.flv [video|audio|meta|all(default)|brief]')
        exit()
    if len(sys.argv) > 2:
        print_info(sys.argv[1], sys.argv[2])
    else:
        print_info(sys.argv[1], 'all')

