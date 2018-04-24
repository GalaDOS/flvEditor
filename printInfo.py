#!/usr/bin/env python3
#coding=utf-8

import os
import sys
from FlvMuxer import *

if __name__ == '__main__':
    muxer = FlvMuxer()
    if len(sys.argv) < 2:
        print('Please specify the input file')
        print('Usage: ./printInfo.py input.flv [video|audio|meta|all(default)]')
        exit()
    if len(sys.argv) > 2:
        if sys.argv[2] not in type_code:
            print('Invalid type specified')
            exit()
        target_type = type_code[sys.argv[2]]
    else:
        target_type = 0

    muxer.open_input_file(sys.argv[1])
    l = muxer.get_tag_list()
    for tag in l:
        if target_type == 0 or tag.type == target_type:
            print('No: ', tag.index, ', type: ', tag.type, ', timestamp: ', tag.timestamp, ', size: ', tag.size)

