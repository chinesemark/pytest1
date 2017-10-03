# -*- coding: utf-8 -*-
__author__ = 'wangweijun'
__daytime__ = '2015-08-24'
__module__  = '�Ա��ı�����'
import difflib
import sys
try:
    textfile1 = sys.argv[1]
    textfile2 = sys.argv[2]

except Exception,e:
    print "Error:" +str(e)
    print"Usage:compare_content_diff.py filename1 filename2"
    sys.exit()

def readline(filename):
    try:
        fileHandle = open(filename,'rb')
        text = fileHandle.read().splitlines()
        fileHandle.close()
        return text
    except IOError as error:
        print ('Read file Error:' +str(error))
        sys.exit()

if textfile1 == "" or textfile2 == "":
    print "Usage:compare_content_diff.py filename1 filename"
    sys.exit()

text1_lines = readline(textfile1)
text2_lines = readline(textfile2)

d = difflib.HtmlDiff()
print d.make_file(text1_lines,text2_lines)