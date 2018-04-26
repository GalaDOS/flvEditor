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
