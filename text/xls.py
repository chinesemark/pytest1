# -*- coding: utf-8 -*-

import xlrd
import sys

print sys.getdefaultencoding()

path = 'E:\huabian/9.22/9.22.xlsx'
path1 = path.decode('utf8')
data = xlrd.open_workbook(path1)
for k in range(len(data.sheets())):
    table = data.sheet_by_index(k)
    print table
    nrows = table.nrows
    ncols = table.ncols

    for i in xrange(nrows):
          print table.row_values(i)[0],table.row_values(i)[1],table.row_values(i)[2],table.row_values(i)[3],table.row_values(i)[4]

