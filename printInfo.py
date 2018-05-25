#!/usr/bin/env python3
#coding=utf-8

import os
import sys
from FlvMuxer import *

def print_info(input_filename, target_type, target_time):
    target_code = 0
    if target_type in type_code:
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
        if target_time != 0 and tag.timestamp > target_time * 1000:
            break
        if target_type == 'all' or tag.type == target_code:
            if tag.type in code_type:
                type_print = code_type[tag.type]
            else:
                type_print = 'unknown'
            print('No: ', tag.index, ', type: ', type_print, ', timestamp: ', tag.timestamp, ', size: ', tag.size, ', detail: ', tag.data_info)

def parse_argv():
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        return None
    result = {'type': 'all', 'time': '0'}
    if len(sys.argv) == 2:
        return result
    if len(sys.argv) == 3:
        if sys.argv[2] == 'all' or sys.argv[2] == 'brief' or sys.argv[2] in type_code:
            result['type'] = sys.argv[2]
            return result
        elif sys.argv[2].isdigit():
            result['time'] = sys.argv[2]
            return result
        return None
    if sys.argv[2] == 'all' or sys.argv[2] == 'brief' or sys.argv[2] in type_code:
        if sys.argv[3].isdigit():
            result['type'] = sys.argv[2]
            result['time'] = sys.argv[3]
            return result
    elif sys.argv[2].isdigit():
        if sys.argv[3] == 'all' or sys.argv[3] == 'brief' or sys.argv[3] in type_code:
            result['type'] = sys.argv[3]
            result['time'] = sys.argv[2]
            return result
    return None


if __name__ == '__main__':
    opt = parse_argv()
    if not opt:
        print('Please specify the input file')
        print('Usage:       ./printInfo.py input.flv [video|audio|meta|all(default)|brief] [N]')
        print('Options:')
        print('video:       print video tags')
        print('audio:       print audio tags')
        print('meta:        print meta tags')
        print('all:         print all tags')
        print('brief:       only print basic info')
        print('N(number):   only print tags in the first N second')
        print('Example:     ./printInfo.py input.flv video 1000')
        exit()

    print_info(sys.argv[1], opt['type'], int(opt['time']))

