#!/usr/bin/python
# -*- coding:utf8 -*-

import sys
import os
import re

print sys.getdefaultencoding()
def search_files (path):
    num = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            print os.path.join(root, name).decode('gbk')
            sn = root.split('\\')[-1]
            print re.findall(".jpg",name)

            print sn
            num +=1

    print num
if __name__ == "__main__":
    path = 'e:\huabian\9.22'
    search_files(path)