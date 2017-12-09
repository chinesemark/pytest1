# -*- coding: UTF-8 -*-
import xlrd
import time
from os import listdir
from os.path import isfile, join
import json

"""
功能：遍历一个文件夹下的所有excel文件，并对其进行去重处理，再存储到一个文本文件中（每一行都是一个json字符串）
"""

path = './'
# {编号：['名称', '工艺', '成份', '尺寸']}
result_map = {}
# 计数器，不做去重情况下的所有item的总数
process_item_count = 0


def process_one_file(file_path):
    global process_item_count
    print(file_path)
    data = xlrd.open_workbook(file_path)
    sheets = data.sheets()
    for table in sheets:
        nrows = table.nrows
        for i in range(1,nrows):
            values = table.row_values(i)
            result_map[values[0]] = values[1:]
            process_item_count += 1


def process(path):
    file_items = [f for f in listdir(path)]
    for item in file_items:
        file_path = join(path, item)
        if isfile(file_path):
            if item.lower().endswith('.xlsx') or item.lower().endswith('.xls'):
                if item.lower().startswith('~$'):
                    continue
                process_one_file(file_path)
        else:
            process(file_path)

if __name__ == "__main__":
    process(path)
    current_time = 'xlsx_process_result_' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.txt'
    result_path = join(path, current_time)
    with open(result_path,'w', encoding='utf8') as outputfile:
        for key in result_map:
            result_json_line = {key:result_map[key]}
            outputfile.write(json.dumps(result_json_line, ensure_ascii=False)+'\n')
    print('process done.')
    print('total count:'+str(process_item_count))
