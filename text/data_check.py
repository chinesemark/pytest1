# -*- coding: UTF-8 -*-
import xlrd
import time
from os import listdir
from os.path import isfile, isdir, join, exists, basename
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

# 所有图片
all_items = []

file_count = 0
item_count = 0
image_count = 0
image_total_count = 0

# 从指定的Excel文件中取出所有Code（未去重）
def get_codes_from_file(file_path):
    results = []
    data = xlrd.open_workbook(file_path)
    sheets = data.sheets()
    for table in sheets:
        print('processing sheet : ' + table.name)

        nrows = table.nrows
        if nrows == 0:
            print('No data in ' + table.name)
            continue

        for i in range(1, nrows):
            values = table.row_values(i)
            results.append(values[0])

    return results

# 在指定目录下查找Code对应的图片存放的文件夹路径
def find_image_path(current_path, code):
    target_path = ''

    expected_path = join(current_path, code)
    if exists(expected_path):
        target_path = expected_path
    else:
        dir_items = [f for f in listdir(current_path)]
        if invalid_folder in dir_items:
            dir_items.remove(invalid_folder)

        for dir_item in dir_items:
            next_path = join(current_path, dir_item)
            if isdir(next_path):
                expected_path = find_image_path(next_path, code)
                if expected_path != '':
                    target_path = expected_path
                    break

    return target_path

# 获取指定目录下的所有包含图片的文件夹路径，图片数量不限
def get_all_image_folder_paths(current_path):
    results = []
    dir_items = [f for f in listdir(current_path)]
    if invalid_folder in dir_items:
        dir_items.remove(invalid_folder)
    for dir_item in dir_items:
        next_path = join(current_path, dir_item)

        # 如果是文件，并且是以'.jpg'为后缀，并且没有重复过
        if isfile(next_path) and dir_item.lower().endswith('.jpg') and current_path not in results:
            results.append(current_path)

        # 如果是文件夹，则遍历下一层级目录
        if isdir(next_path):
            next_results = get_all_image_folder_paths(next_path)
            results.extend(next_results)

    return results

# 校对数据，以Excel所在目录为根目录，校对当前目录下图片与Excel中的数据是否一致
def check_datas(path, item):
    global file_count
    global item_count

    file_count += 1

    file_path = join(path, item)
    print('processing file : ' + file_path)

    # 获取当前sheet下的所有code
    results = get_codes_from_file(file_path)
    all_items.extend(results);
    # 累计item数
    item_count += len(results)

    for code in results:
        image_folder_path = find_image_path(path, code)
        # 图片文件夹不存在
        if image_folder_path == '':
            result = file_path + ' -> ' + code
            image_not_exists_list.append(result)
        else:
            image_files = [f for f in listdir(image_folder_path)]
            if invalid_folder in image_files:
                image_files.remove(invalid_folder)
            # 文件夹下有5个文件(夹)
            if len(image_files) == 5:
                count = 0
                for image_file in image_files:
                    image_file_path = join(image_folder_path, image_file)
                    print('checking image... : ' + image_file_path)
                    try:
                        Image.open(image_file_path)
                        count += 1
                        print('OK')
                    except:
                        print('Error openning')

                # 文件夹下有效的图片不足5张
                if count != 5:
                    image_invalid_list.append(image_folder_path)
            else:
                # 文件夹下"图片"数量不足5
                image_count_invalid_list.append(image_folder_path)

def process(path):
    file_items = [f for f in listdir(path)]
    for item in file_items:
        file_path = join(path, item)
        if isfile(file_path):
            if item.lower().endswith('.xlsx') or item.lower().endswith('.xls'):
                if item.lower().startswith('~$'):
                    continue
                check_datas(path, item)
        else:
            process(file_path)

def process_images(path):
    global image_count
    global image_total_count

    # 反过来获取目录下所有的图片文件夹
    all_image_folders = get_all_image_folder_paths(path)

    # 累计图片文件夹的数量
    image_count += len(all_image_folders)

    for image_folder_path in all_image_folders:
        if isfile(image_folder_path):
            continue

        # 累计图片文件夹下"图片"的数量
        image_items = [f for f in listdir(image_folder_path)]
        if invalid_folder in image_items:
            image_items.remove(invalid_folder)

        for item in image_items:
            if item.lower().endswith('.jpg'):
                image_total_count += 1
        # image_total_count += len(image_items)

        # 有图片，但Excel里没有对应的code
        if basename(image_folder_path) not in all_items:
            item_not_exists_list.append(image_folder_path)

def write_results_to_file():
    current_time = 'result_' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.txt'
    output_path = join(result_path, current_time)

    with open(output_path, 'w', encoding='utf8') as outputfile:
        outputfile.write('Excel中有数据，但同目录下没有该编号对应的图片(文件夹): ' + str(len(image_not_exists_list)) + '项\n')
        outputfile.write('-------------------------\n')
        for r in image_not_exists_list:
            outputfile.write(r + '\n')
        outputfile.write('-------------------------\n')

        outputfile.write('\n')
        outputfile.write('Excel中有数据，同目录下存在该编号对应的图片(文件夹)，但图片数量不等于5张: ' + str(len(image_count_invalid_list)) + '项\n')
        outputfile.write('-------------------------\n')
        for r in image_count_invalid_list:
            outputfile.write(r + '\n')
        outputfile.write('-------------------------\n')

        outputfile.write('\n')
        outputfile.write('Excel中有数据，同目录下存在该编号对应的图片(文件夹)，数量是5张，但图片格式无效，无法打开: ' + str(len(image_invalid_list)) + '项\n')
        outputfile.write('-------------------------\n')
        for r in image_invalid_list:
            outputfile.write(r + '\n')
        outputfile.write('-------------------------\n')

        outputfile.write('\n')
        outputfile.write('同目录下有图片(文件夹)，但是Excel中没有对应的编号数据: ' + str(len(item_not_exists_list)) + '项\n')
        outputfile.write('-------------------------\n')
        for r in item_not_exists_list:
            outputfile.write(r + '\n')
        outputfile.write('-------------------------\n')

        outputfile.write('\n')
        outputfile.write('共扫描到 ' + str(file_count) + ' 个Excel，Excel中数据 ' + str(item_count) + ' 项，图片文件夹 ' + str(image_count) + ' 项，图片文件数 ' + str(
            image_total_count) + ' 项')

def print_results():
    print('\033[31m')
    print('\n')
    print('Excel中有数据，但同目录下没有该编号对应的图片(文件夹): ' + str(len(image_not_exists_list)) + '项')
    print('-------------------------')
    for r in image_not_exists_list:
        print(r)
    print('-------------------------')

    print('\n')
    print('Excel中有数据，同目录下存在该编号对应的图片(文件夹)，但图片数量不等于5张: ' + str(len(image_count_invalid_list)) + '项')
    print('-------------------------')
    for r in image_count_invalid_list:
        print(r)
    print('-------------------------')

    print('\n')
    print('Excel中有数据，同目录下存在改编号对应的图片(文件夹)，数量是5张，但图片格式无效，无法打开: ' + str(len(image_invalid_list)) + '项')
    print('-------------------------')
    for r in image_invalid_list:
        print(r)
    print('-------------------------')

    print('\n')
    print('同目录下有图片(文件夹)，但是Excel中没有对应的编号数据: ' + str(len(item_not_exists_list)) + '项')
    print('-------------------------')
    for r in item_not_exists_list:
        print(r)
    print('-------------------------')

    print('\n')
    print('共扫描到 ' + str(file_count) + ' 个Excel，Excel中数据 ' + str(item_count) + ' 项，图片文件夹 ' + str(image_count) + ' 项，图片文件数 ' + str(image_total_count) + ' 项')

    print('\033[0m')


if __name__ == "__main__":
    process(path)
    process_images(path)
    write_results_to_file()
    print_results()
    print('process done.')
