# coding = utf-8

# 532译码脚本
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '532Decoder.bin')

with open(filename, 'wb') as file:
    for var in range(32):
        value = 1 << var
        result = value.to_bytes(4, byteorder='little')
        file.write(result)