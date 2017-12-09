# -*- coding: utf-8 -*-


import os
from PIL import Image

def search_files (path):
    imglist = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.jpg'):
               imglist.append(os.path.join(root, name).decode('gbk'))

    return  imglist




path = 'E:\huabian\9.22'
#path1 = path.decode('utf8')
search_files(path)

for img in search_files(path):
  print img
  try:
    img = Image.open(img)
    img.rotate(45)
    img.transpose(Image.ROTATE_90)
    img.show()
    print img.format, img.size, img.mode
  except IOError:
    print "cannot convert=========================" + img



