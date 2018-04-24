#!/usr/bin/env python3
#coding=utf-8

import os
import sys

type_code = {'meta':18, 'video': 9, 'audio': 8, 'all': 0}

class FlvTag():
    def __init__(self):
        self.index = 0
        self.type = 0
        self.size = 0
        self.timestamp = 0
        self.position = 0
        self.data = b''
        self.data_info = ''



class FlvMuxer():

    def __init__(self):
        self.input_filename = ''
        self.output_filename = ''
        self.input_file = None
        self.output_file = None
        self.tag_index = 0
        self.write_header_flag = False

    def __del__(self):
        if self.input_file is not None:
            self.input_file.close()
        if self.output_file is not None:
            self.output_file.close()

    def open_input_file(self, filename):
        self.input_filename = filename
        try:
            self.input_file = open(filename, 'rb')
        except Exception:
            print('Unable to open input file: ', filename)
            self.input_file = None
            return False
        return self.__skip_flv_header()

    def open_output_file(self, filename, has_video = True, has_audio = True):
        self.output_filename = filename
        try:
            self.output_file = open(filename, 'wb')
        except Exception:
            print('Unable to open output file: ', filename)
            self.output_file = None
            return False
        return self.__write_flv_header(has_video, has_audio)

    def __skip_flv_header(self):
        f = self.input_file
        identity = f.read(3)
        if identity != b'FLV':
            print('Input file is not a FLV file')
            self.input_file.close()
            self.input_file = None
            return False
        f.seek(5)
        byte = f.read(4)
        size = (int(byte[0]) << 24) + (int(byte[1]) << 16) + (int(byte[2]) << 8) + int(byte[3])
        f.seek(size + 4)
        return True

    def __write_flv_header(self, has_video, has_audio):
        f = self.output_file
        header = b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00'
        if not has_video:
            tmp = list(header)
            tmp[4] = 0x04   # pure audio
            header = bytes(tmp)
        elif not has_audio:
            tmp = list(header)
            tmp[4] = 0x01   # pure video
            header = bytes(tmp)
        f.write(header)
        return True

    """
    Read 1 FLV tag
    with_data = True: return complete tag
    with_data = False: return tag infomation only
    """
    def read_tag(self, with_data = False):
        if not self.input_file:
            print('Input file has not been opened')
            return None
        f = self.input_file
        tag = FlvTag()
        header = f.read(11) # tag header
        if not header or len(header) < 11:
            return None

        tag.type = header[0]
        tag.size = (header[1] << 16) + (header[2] << 8) + header[3]
        tag.timestamp = (header[4] << 16) + (header[5] << 8) + (header[6]) + (header[7] << 24)
        tag.position = f.tell() - 11
        self.tag_index += 1
        tag.index = self.tag_index

        if with_data:
            tag.data = f.read(tag.size)
            f.seek(4, 1)
        else:
            f.seek(tag.size + 4, 1)
        return tag

    """
    Write 1 FLV tag
    """
    def write_tag(self, tag):
        if not self.output_file:
            print('Output file has not been opened')
            return False
        if not isinstance(tag, FlvTag) or not isinstance(tag.data, bytes):
            print('Can not recognize the param')
            return False
        if tag.size != len(tag.data):
            print('Invalid tag size')
            return False

        f = self.output_file
        header = [0] * 11
        trailer = [0] * 4
        header[0] = tag.type
        header[1] = (tag.size >> 16) & 0xFF
        header[2] = (tag.size >> 8) & 0xFF
        header[3] = tag.size & 0xFF
        header[4] = (tag.timestamp >> 16) & 0xFF
        header[5] = (tag.timestamp >> 8) & 0xFF
        header[6] = tag.timestamp & 0xFF
        header[7] = (tag.timestamp >> 24 ) & 0xFF

        pre_tag_size = tag.size + 11
        trailer[0] = (pre_tag_size >> 24) & 0xFF
        trailer[1] = (pre_tag_size >> 16) & 0xFF
        trailer[2] = (pre_tag_size >> 8) & 0xFF
        trailer[3] = pre_tag_size & 0xFF

        f.write(bytes(header))
        f.write(tag.data)
        f.write(bytes(trailer))
        return True

    """
    Get a list of tag infomarion
    """
    def get_tag_list(self):
        tag_list = []
        if not self.input_file:
            print('Input file has not been opened')
            return tag_list
        while True:
            item = self.read_tag()
            if not item:
                break
            else:
                tag_list.append(item)
        return tag_list



if __name__ == '__main__':
    muxer = FlvMuxer()
    if len(sys.argv) < 2:
        print('Please specify the input file')
        exit()
    muxer.open_input_file(sys.argv[1])
    l = muxer.get_tag_list()
    for tag in l:
        print('No: ', tag.index, ', type: ', tag.type, ', ts: ', tag.timestamp, ', size: ', tag.size)

