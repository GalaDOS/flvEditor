# flvEditor
Simple flv editing script wirtten in python3.

* **FlvMuxer.py**:

Core class


* **printInfo.py**:

Print movie infomation.

Usage:
`./printInfo.py input.flv [all(default)/video/audio/meta/brief]`


* **edit.py**:

Cut and merge flv movies.

Usage:
`./edit.py -add input1.flv [-ss n(sec)] [-to n(sec)] [-add input2.flv] ... -out output.flv`


* **flv2h264.py**:

Convert a flv file to H.264 stream.

Usage:
`./flv2h264.py input.flv output.264`


* **checkTimestamp.py**:

Check if the timestamp is valid.

Usage:
`./checkTimestamp.py input.flv`
