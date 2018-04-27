#!/usr/bin/env python3
#coding=utf-8

import os
import sys
from FlvMuxer import *

def get_sps_and_pps(tag):
    nauls = []
    data = list(tag.data)[5:] # it's AVCDecoderConfigurationRecord
    number_of_sps = data[5] & 0x1F
    index = 6
    for count in range(number_of_sps):
        length = (data[index] << 8) + data[index+1]
        index += 2
        nauls.append(bytes(data[index:index+length]))
        index += length
    number_of_pps = data[index]
    index += 1
    for count in range(number_of_sps):
        length = (data[index] << 8) + data[index+1]
        index += 2
        nauls.append(bytes(data[index:index+length]))
        index += length
    return nauls


def write_264_stream(f, tag):
    i = 0
    data = list(tag.data)[5:]
    start_code = b'\x00\x00\x00\x01'
    if '264 header' in tag.data_info:
        nauls = get_sps_and_pps(tag)
        for naul in nauls:
            f.write(start_code)
            f.write(naul)
        return
    while i < len(data):
        length = (data[i] << 24) + (data[i+1] << 16) + (data[i+2] << 8) + data[i+3]
        i += 4
        f.write(start_code)
        f.write(bytes(data[i:i+length]))
        i += length


def flv_to_h264(input_filename, output_filename):
    muxer = FlvMuxer()
    if not muxer.open_input_file(input_filename):
        return False
    try:
        f264 = open(output_filename, 'wb')
    except Exception:
        print('Unable to open output file')
        return False
    while True:
        tag = muxer.read_tag(True)
        if not tag:
            break
        if tag.type == type_code['video']:
            if muxer.video_info != 'H.264/AVC':
                print('It\'s not a H.264 video stream')
                return False
            write_264_stream(f264, tag)
    return True


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ./flv2h264.py input.flv output.264')
        exit()
    if flv_to_h264(sys.argv[1], sys.argv[2]):
        print('Done')
    else:
        print('Failed')

