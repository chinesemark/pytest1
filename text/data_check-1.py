# -*- coding: UTF-8 -*-
import xlrd
import time
from os import listdir
from os.path import isfile, join, exists
from PIL import Image

path = './'
result_path = './'
invalid_folder = '.DS_Store'

# 对应的图片不存在
image_not_exists_list = []

# 有图片，但是图片数量不正确
image_count_invalid_list = []

# 有图片，但图片格式不正确，无法打开
image_invalid_list = []

# 有图片，无数据
item_not_exists_list = []

file_count = 0
item_count = 0
image_count = 0
image_total_count = 0

def check_datas(path, item):
    global file_count
    global item_count
    global image_count
    global image_total_count

    file_count += 1

    file_path = join(path,item)
    print('processing file : ' + file_path)

    data = xlrd.open_workbook(file_path)
    sheets = data.sheets()
    for table in sheets:
        print('processing sheet : ' + table.name)

        nrows = table.nrows
        if nrows == 0 :
            print('No data in ' + table.name)
            continue

        # 获取当前sheet下的所有code
        results = []
        for i in range(1, nrows):
            values = table.row_values(i)
            results.append(values[0])

        # 累计item数
        item_count += len(results)

        # 根据获取到的code，去查对应目录下是否有图片(文件夹)
        # 目录名优先匹配当前的sheet名，如果匹配不到，则匹配Excel文件名
        folder_name = table.name
        folder_path = join(path, folder_name)
        if not exists(folder_path):
            end = item.rfind('.')
            folder_name = item[0: int(end)]
            folder_path = join(path, folder_name)

        # 遍历当前sheet下取到的所有code
        for r in results:
            # 拼接图片文件夹路径
            sub_folder_path = join(folder_path, r)

            # 图片文件夹不存在
            if not exists(sub_folder_path):
                image_not_exists_list.append(sub_folder_path)
            else:
                # 图片文件夹存在，判断底下文件数量
                image_items = [f for f in listdir(sub_folder_path)]
                if invalid_folder in image_items:
                    image_items.remove(invalid_folder)

                # 文件夹下有5个文件(夹)
                if len(image_items) == 5:
                    count = 0
                    for image in image_items:
                        image_path = join(sub_folder_path, image)
                        print('checking image... : ' + image_path)
                        try:
                            Image.open(image_path)
                            count += 1
                            print('OK')
                        except:
                            print('Error openning')

                    # 文件夹下有效的图片不足5张
                    if count != 5:
                        image_invalid_list.append(sub_folder_path)
                else:
                    # 文件夹下"图片"数量不足5
                    image_count_invalid_list.append(sub_folder_path)

        # 反过来获取目录下所有的图片文件夹
        all_image_items = []
        if exists(folder_path):
            all_image_items = [f for f in listdir(folder_path)]
            if invalid_folder in all_image_items:
                all_image_items.remove(invalid_folder)

        # 累计图片文件夹的数量
        image_count += len(all_image_items)

        for image in all_image_items:
            sub_folder_path = join(folder_path, image)
            if isfile(sub_folder_path):
                continue

            # 累计图片文件夹下"图片"的数量
            image_items = [f for f in listdir(sub_folder_path)]
            if invalid_folder in image_items:
                image_items.remove(invalid_folder)
            image_total_count += len(image_items)

            # 有图片，但Excel里没有对应的code
            if image not in results:
                item_not_exists_list.append(sub_folder_path)

def process(path):
    file_items = [f for f in listdir(path)]
    for item in file_items:
        file_path = join(path, item)
        if isfile(file_path):
            if item.find('.xlsx') > -1 or item.find('.xls') > -1:
                check_datas(path, item)
        else:
            process(file_path)



def write_results_to_file():
    current_time = 'result_' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.txt'
    output_path = join(result_path, current_time)

    with open(output_path, 'w', encoding='utf8') as outputfile:
        outputfile.write('Excel中有数据，但目录下没有对应的图片(文件夹): ' + str(len(image_not_exists_list)) + '项\n')
        outputfile.write('-------------------------\n')
        for r in image_not_exists_list:
            outputfile.write(r + '\n')
        outputfile.write('-------------------------\n')

        outputfile.write('\n')
        outputfile.write('Excel中有数据，目录下对应的图片(文件夹)，但图片数量不等于5张: ' + str(len(image_count_invalid_list)) + '项\n')
        outputfile.write('-------------------------\n')
        for r in image_count_invalid_list:
            outputfile.write(r + '\n')
        outputfile.write('-------------------------\n')

        outputfile.write('\n')
        outputfile.write('Excel中有数据，目录下对应的图片(文件夹)，数量是5张，但图片格式无效，无法打开: ' + str(len(image_invalid_list)) + '项\n')
        outputfile.write('-------------------------\n')
        for r in image_invalid_list:
            outputfile.write(r + '\n')
        outputfile.write('-------------------------\n')

        outputfile.write('\n')
        outputfile.write('目录下有图片(文件夹)，但是Excel中没有对应的数据: ' + str(len(item_not_exists_list)) + '项\n')
        outputfile.write('-------------------------\n')
        for r in item_not_exists_list:
            outputfile.write(r + '\n')
        outputfile.write('-------------------------\n')

        outputfile.write('\n')
        outputfile.write('共扫描到 ' + str(file_count) + '个Excel，Excel中数据 ' + str(item_count) + ' 项，Excel对应的图片文件夹 ' + str(image_count) + ' 项，图片文件数 ' + str(
            image_total_count) + ' 项')

def print_results():
    print('\033[31m')
    print('\n')
    print('Excel中有数据，但目录下没有对应的图片(文件夹): ' + str(len(image_not_exists_list)) + '项')
    print('-------------------------')
    for r in image_not_exists_list:
        print(r)
    print('-------------------------')

    print('\n')
    print('Excel中有数据，目录下对应的图片(文件夹)，但图片数量不等于5张: ' + str(len(image_count_invalid_list)) + '项')
    print('-------------------------')
    for r in image_count_invalid_list:
        print(r)
    print('-------------------------')

    print('\n')
    print('Excel中有数据，目录下对应的图片(文件夹)，数量是5张，但图片格式无效，无法打开: ' + str(len(image_invalid_list)) + '项')
    print('-------------------------')
    for r in image_invalid_list:
        print(r)
    print('-------------------------')

    print('\n')
    print('目录下有图片(文件夹)，但是Excel中没有对应的数据: ' + str(len(item_not_exists_list)) + '项')
    print('-------------------------')
    for r in item_not_exists_list:
        print(r)
    print('-------------------------')

    print('\n')
    print('共扫描到 ' + str(file_count) + '个Excel，Excel中数据 ' + str(item_count) + ' 项，Excel对应的图片文件夹 ' + str(image_count) + ' 项，图片文件数 ' + str(image_total_count) + ' 项')

    print('\033[0m')


if __name__ == "__main__":
    process(path)
    write_results_to_file()
    print_results()
    print('process done.')
