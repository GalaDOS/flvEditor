#!/usr/bin/env python3
#coding=utf-8

import os
import sys
from FlvMuxer import *

def check_timestamp(input_filename):
    cur_ts = {'video': -1, 'audio': -1}
    cur_global_ts = 0

    code_type = {18:'meta', 8: 'audio', 9: 'video'}
    muxer = FlvMuxer()
    if not muxer.open_input_file(input_filename):
        return
    l = muxer.get_tag_list()
    for tag in l:
        if tag.type in code_type:
            type_str = code_type[tag.type]
        else:
            type_str = 'unknown'
        if cur_global_ts > tag.timestamp:
            print('Warning: non-monotonous global timestamp. Type: ', type_str, ' timestamp: ', tag.timestamp, ' previous: ', cur_global_ts)
        cur_global_ts = tag.timestamp

        if type_str in cur_ts:
            if cur_ts[type_str] > tag.timestamp:
                print('Error: backward timestamp in {} stream, current: {}, previous: {}'.format(type_str, tag.timestamp, cur_ts[type_str]))
            elif cur_ts[type_str] == tag.timestamp:
                print('Warning: same timestamp in ', type_str, 'stream: ', tag.timestamp)
            cur_ts[type_str] = tag.timestamp


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: ./checkTimestamp.py input.flv')
        exit()
    check_timestamp(sys.argv[1])

