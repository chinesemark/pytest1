#!/usr/bin/python
# -*- coding:utf8 -*-

import os

def search_files (path):
    num = 0
    for root , dirs, files in os.walk(path):
        for name in files:
            print os.path.join(root, name).decode('gbk')
            sn = root.split('\\')[-1]
            num1 = 0
            if sn is sn:
                num1 += 1
            print num1
            num += 1
    print num
if __name__ == "__main__":
    path = 'e:\huabian\9.22'
    search_files(path)