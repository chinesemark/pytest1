# -*- coding: utf-8 -*-
import xlrd
import sys

print sys.getdefaultencoding()


data = xlrd.open_workbook('e:/hb/execl/9.1.xlsx')

table = data.sheet_by_name(u'Sheet1')

nrows = table.nrows
ncols = table.ncols

for i in xrange(nrows):
    print table.row_values(i)[0],table.row_values(i)[1],table.row_values(i)[2],table.row_values(i)[3],table.row_values(i)[4]



