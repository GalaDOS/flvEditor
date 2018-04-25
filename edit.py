#!/usr/bin/env python3
#coding=utf-8

import os
import sys
from FlvMuxer import *

def parse_argv_for_edit(input_filename, start_time, end_time, output_filename):
    i = 1
    count = -1
    while i < len(sys.argv) - 1:
        opt = sys.argv[i]
        value = sys.argv[i+1]
        i += 2
        if opt == '-add':
            count += 1
            input_filename.append(value)
            start_time.append(0)
            end_time.append(0)
        elif opt == '-ss':
            if count >= 0:
                start_time[count] = int(value)
        elif opt == '-to':
            if count >= 0:
                end_time[count] = int(value)
        elif opt == '-out':
            output_filename.append(value)
        else:
            return False

    if count < 0 or len(output_filename) != 1:
        return False
    return True

"""
input_filename:     list, length should be larger than 0
start_time:         list, 0 means no cut at the beginning
end_time:           list, 0 means no cut at the end
output_filename:    string
"""
def edit_flv(input_filename, start_time, end_time, output_filename):
    muxer = FlvMuxer()
    print(input_filename)
    print(start_time)
    print(end_time)
    print(output_filename)


if __name__ == '__main__':
    input_filename = []
    start_time = []
    end_time = []
    output_filename = []
    if not parse_argv_for_edit(input_filename, start_time, end_time, output_filename):
        print('Usage: ./edit.py -add input1.flv [-ss n(sec)] [-to n(sec)] [-add input2.flv] ... -out output.flv')
        exit()
    edit_flv(input_filename, start_time, end_time, output_filename[0])

