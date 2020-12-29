# -*- coding: UTF-8 -*-
import zip2word, word2md, textMatch, textMatch2
import os
import pprint
import json
import csv
import time

# 获取list中entity_type，保存在dict的entity_type；获取entity，保存在entity
def getContent(r_list):
    entity_list = []
    for i in r_list['entity_list']:
        result = {'entity_type': '', 'entity': ''}
        result['entity_type'] = r_list['entity_list'][i]['entity_type']
        result['entity'] = r_list['entity'][i]['entity']
        entity_list.append(result)
    return entity_list


# 表头
def getHeaders():
    # 表头
    headers = ['文件名', '投资目标', '投资范围', '投资策略', '业绩比较基准', '风险收益特征']
    header_file = open('entitySchemas.json', 'r').read()
    header_json = json.loads(header_file)
    for i in header_json['entitySchemas']:
        headers.append(i['entityType'])
    return headers


# 合并两个list
def mergeList(r_list1, r_list2):
    return r_list1 + r_list2


# 标准化list，合并两个list，空值置None
def stdList(r_list):
    entity_list = []
    for j in getHeaders():
        tmp_count = 0
        for i in r_list:
            if j == i['entity_type']:
                entity_list.append(i['entity'])
                tmp_count += 1
        if tmp_count == 0:
            entity_list.append('None')
    print("entity_list：", entity_list)
    return entity_list

# list转csv
def list2csv(result_list, result_file):
    headers = getHeaders()
    # 写入内容
    f = open('result/' + result_file, 'w')
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    all_list = []
    for entity_list in result_list:
        all_list.append(entity_list)
    f_csv.writerows(all_list)


# main：输入zip，输出csv
def zip2csv(zip_file, zip_filename, result_file):
    url = "http://172.27.128.117:5022/api/word2md"
    zip2word.UPLOAD_PATH = './upload/'
    zip2word.RESULT_PATH = './result/'
    zip2word.unzip(zip_file, zip_filename)
    result_list = []  # 外层list是所有的文本list，内层list是一个文本内所有entity的信息
    for root, dir, files in os.walk(zip2word.UPLOAD_PATH + zip_filename):
        for file in files:
            file_name = os.path.join(root, file)
            string = word2md.word2string(url, file_name)
            list1 = textMatch.main(string)
            list2 = textMatch2.str2list(string)
            fname_list = [{'entity_type': '文件名', 'entity': file}]
            r_list = fname_list + list1 + list2
            entity_list = stdList(r_list)
            result_list.append(entity_list)
    list2csv(result_list, result_file)  # 暂时存在result.csv中


if __name__ == '__main__':
    zip_file = open('line1.zip', 'rb')
    zip_filename = 'line1'
    result_file = zip_filename + '.csv'
    zip2csv(zip_file, zip_filename, result_file)