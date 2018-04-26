#!/usr/bin/env python3
#coding=utf-8

import os
import sys
from FlvMuxer import *

def parse_argv_for_edit(input_filenames, start_times, end_times, output_filename):
    i = 1
    count = -1
    while i < len(sys.argv) - 1:
        opt = sys.argv[i]
        value = sys.argv[i+1]
        i += 2
        if opt == '-add':
            count += 1
            input_filenames.append(value)
            start_times.append(0)
            end_times.append(0)
        elif opt == '-ss':
            if count >= 0:
                start_times[count] = int(value) * 1000 # from sec to ms
        elif opt == '-to':
            if count >= 0:
                end_times[count] = int(value) * 1000   # from sec to ms
        elif opt == '-out':
            output_filename.append(value)
        else:
            return False

    if count < 0 or len(output_filename) != 1:
        return False
    return True

"""
input_filenames:    list, length should be larger than 0
start_times:        list, 0 means no cut at the beginning
end_times:          list, 0 means no cut at the end
output_filename:    string
"""
def edit_flv(input_filenames, start_times, end_times, output_filename):
    muxer = FlvMuxer()
    print('input filenames: ', input_filenames)
    print('start times: ', start_times)
    print('end_times: ', end_times)
    print('output filename: ', output_filename)
    if not muxer.open_output_file(output_filename):
        return False
    muxer.write_empty_meta()
    first_video_header = None
    first_audio_header = None
    cur_timestamp = 0
    timestamp_offset = 0
    for i in range(len(input_filenames)):
        wait_keyframe = True
        muxer.open_input_file(input_filenames[i])
        while True:
            tag = muxer.read_tag(True)
            if not tag:
                break
            tag.timestamp += timestamp_offset
            if cur_timestamp < tag.timestamp:
                cur_timestamp = tag.timestamp
            if tag.type == type_code['video']:
                if '264 header' in tag.data_info:
                    if not first_video_header:
                        first_video_header = tag
                        muxer.write_tag(tag)
                    elif first_video_header.data != tag.data:
                        print('Warning: most video player do not support playing a video with multiple encoding parameters.',
                                'You should transcode the input files before merging. Try ffmpeg\'s concat filter.')
                        muxer.write_tag(tag)
                elif tag.timestamp >= start_times[i] + timestamp_offset and (end_times[i] == 0 or tag.timestamp <= end_times[i]):
                    if muxer.video_info == 'H.264/AVC' or muxer.video_info == 'Sorenson H.263':
                        if 'key frame' in tag.data_info:
                            wait_keyframe = False
                        if not wait_keyframe:
                            muxer.write_tag(tag)
                    else:
                        muxer.write(tag)
            elif tag.type == type_code['audio']:
                if 'AAC header' in tag.data_info:
                    if not first_audio_header:
                        first_audio_header = tag
                        muxer.write_tag(tag)
                elif tag.timestamp >= start_times[i] + timestamp_offset and (end_times[i] == 0 or tag.timestamp <= end_times[i]):
                    muxer.write_tag(tag)
        timestamp_offset = cur_timestamp
        muxer.close_input_file()
    return True


if __name__ == '__main__':
    input_filenames = []
    start_times = []
    end_times = []
    output_filename = []
    if not parse_argv_for_edit(input_filenames, start_times, end_times, output_filename):
        print('Usage: ./edit.py -add input1.flv [-ss n(sec)] [-to n(sec)] [-add input2.flv] ... -out output.flv')
        exit()
    if edit_flv(input_filenames, start_times, end_times, output_filename[0]):
        print('Done')
    else:
        print('Failed')

