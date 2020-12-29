# -*- coding: UTF-8 -*-
import json
import re,os
import word2md, zip2word
from pprint import pprint

MAXINT = 2147483647

# txt转string
def readTxt(filename):
    f = open(filename, "r", encoding='utf-8')
    data = f.read()
    return data


# 正则匹配规则--投资目标
def re1(data):
    dictObj = {'entity_type': '投资目标', 'entity': '', 'entity_index': {'begin': MAXINT, 'end': 0}}
    pattern = r'[（(]{0,}[一二三四五六七八九十][）)、]{1}[\s]{0,}投资目标(.*?)[（(]{0,}[二三四五六七八九十][）)、]{1}'
    p = re.compile(pattern, re.DOTALL)
    entity = ''
    for m in p.finditer(data):
        dictObj['entity_index'] = {
            'begin': m.start() if m.start() < dictObj['entity_index']['begin'] else dictObj['entity_index']['begin'],
            'end': m.end() if m.end() > dictObj['entity_index']['end'] else dictObj['entity_index']['end']}
        entity += m.group()
    entity = entity.lstrip(r'[（(]{0,}[一二三四五六七八九十][）)、]{1}[\s]{0,}投资目标[\s]{0,}')
    entity = entity.rstrip(r'[（(]{0,}[一二三四五六七八九十][）)、]{1}')
    entity = entity.replace('\n', '')
    dictObj['entity'] = entity
    if len(entity) == 0:
        dictObj = None
    return dictObj


# 正则匹配规则--投资范围
def re2(data):
    dictObj = {'entity_type': '投资范围', 'entity': '', 'entity_index': {'begin': MAXINT, 'end': 0}}
    pattern = r'[（(]{0,1}[一二三四五六七八九十][）)、]{1}[\s]{0,}(投资范围|投资方向|投资对象及投资范围){1}(.*?)[（(]{0,1}[二三四五六七八九十][）)、]{1}'
    p = re.compile(pattern, re.DOTALL)
    entity = ''
    for m in p.finditer(data):
        dictObj['entity_index'] = {
            'begin': m.start() if m.start() < dictObj['entity_index']['begin'] else dictObj['entity_index']['begin'],
            'end': m.end() if m.end() > dictObj['entity_index']['end'] else dictObj['entity_index']['end']
        }
        entity += m.group()
    entity = entity.lstrip(r'[（(]{0,}[一二三四五六七八九十][）)、]{1}(投资范围|投资方向|投资对象及投资范围){1}[\s]{0,}')
    entity = entity.rstrip(r'[（(]{0,}[一二三四五六七八九十][）)、]{1}')
    entity = entity.replace('\n', '')
    dictObj['entity'] = entity
    if len(entity) == 0:
        dictObj = None
    return dictObj


# 正则匹配规则--投资策略
def re3(data):
    dictObj = {'entity_type': '投资策略', 'entity': '', 'entity_index': {'begin': MAXINT, 'end': 0}}
    pattern = r'[（(]{0,}[一二三四五六七八九十][）)、]{1}(\s*)投资策略(.*?)1[、|.]{1}'
    p = re.compile(pattern, re.DOTALL)
    entity = ''
    # 投资策略和1、之间有内容时直接输出这段，若之间只有空行，则输出投资策略下所有内容
    for m in p.finditer(data):
        if m.group().lstrip(r'[（(]{0,}[一二三四五六七八九十][）)、]{1}(\s*?)投资策略').rstrip(r'1[、|.]{1}').replace('\n', '') == '':
            pattern = r'[（(]{0,}[一二三四五六七八九十][）)、]{1}[\s]{0,}(投资策略){1}(.*?)[（(]{0,}[二三四五六七八九十][）)、]{1}'
            p = re.compile(pattern, re.DOTALL)
    for m in p.finditer(data):
        dictObj['entity_index'] = {
            'begin': m.start() if m.start() < dictObj['entity_index']['begin'] else dictObj['entity_index']['begin'],
            'end': m.end() if m.end() > dictObj['entity_index']['end'] else dictObj['entity_index']['end']
        }
        entity += m.group()
    entity = entity.lstrip(r'[（(]{0,}[一二三四五六七八九十][）)、]{1}(\s*?)投资策略')
    entity = entity.rstrip(r'1[、|.]{1}')
    entity = entity.rstrip(r'[（(]{0,}[一二三四五六七八九十][）)、]{1}')
    entity = entity.replace('\n', '')
    dictObj['entity'] = entity
    if len(entity) == 0:
        dictObj = None
    return dictObj


# 正则匹配规则--业绩比较基准
def re4(data):
    dictObj = {'entity_type': '业绩比较基准', 'entity': '', 'entity_index': {'begin': MAXINT, 'end': 0}}
    pattern = r'[（(]{0,}[一二三四五六七八九十][）)、]{1}(\s*)(业绩比较基准|业绩基准){1}(\s*)(.*?)[\s]'
    p = re.compile(pattern, re.DOTALL)
    entity = ''
    for m in p.finditer(data):
        dictObj['entity_index'] = {
            'begin': m.start() if m.start() < dictObj['entity_index']['begin'] else dictObj['entity_index']['begin'],
            'end': m.end() if m.end() > dictObj['entity_index']['end'] else dictObj['entity_index']['end']
        }
        entity += m.group()
    entity = entity.lstrip(r'[（(]{0,}[一二三四五六七八九十][）)、]{1}(业绩比较基准|业绩基准){1}')
    entity = entity.rstrip(r'[（(]{0,}[一二三四五六七八九十][）)、]{1}')
    entity = entity.replace('\n', '')
    dictObj['entity'] = entity
    if len(entity) == 0:
        dictObj = None
    return dictObj


# 正则匹配规则--风险收益特征
def re5(data):
    dictObj = {'entity_type': '风险收益特征', 'entity': '', 'entity_index': {'begin': MAXINT, 'end': 0}}
    pattern = r'[（(]{0,}[一二三四五六七八九十][）)、]{1}[\s]{0,}(风险收益特征|基金的风险收益特征){1}(.*?)[（(]{0,}[二三四五六七八九十][）)、]{1}'
    p = re.compile(pattern, re.DOTALL)
    entity = ''
    for m in p.finditer(data):
        dictObj['entity_index'] = {
            'begin': m.start() if m.start() < dictObj['entity_index']['begin'] else dictObj['entity_index']['begin'],
            'end': m.end() if m.end() > dictObj['entity_index']['end'] else dictObj['entity_index']['end']
        }
        entity += m.group()
    entity = entity.lstrip(r'[（(]{0,}[一二三四五六七八九十][）)、]{1}(风险收益特征|基金的风险收益特征){1}')
    entity = entity.rstrip(r'[（(]{0,}[一二三四五六七八九十][）)、]{1}')
    entity = entity.replace('\n', '')
    dictObj['entity'] = entity
    if len(entity) == 0:
        dictObj = None
    return dictObj


# main
def main(data):
    # data = readTxt(filename)
    # 将5个匹配的项加到list中
    r_list = []
    r_list.append(re1(data))
    r_list.append(re2(data))
    r_list.append(re3(data))
    r_list.append(re4(data))
    r_list.append(re5(data))
    r_list = list(filter(None, r_list))

    jsonObj = json.dumps(r_list, indent=1, ensure_ascii=False)
    return r_list

    # 结果写入文件
    # f = open('result/' + filename[7:] + "_result.txt", "w", encoding='utf-8')
    # f.write(jsonObj)


# 测试
if __name__ == '__main__':
    # url = "http://172.27.128.117:5022/api/word2md"
    # zip2word.UPLOAD_PATH = './upload/'
    # zip2word.RESULT_PATH = './result/'
    # result_name = '20180608_000062_银华量化智慧动力灵活配置混合型证券投资基金更新招募说明书（2018年第1号）.txt'
    # input_file = open('20180608_000062_银华量化智慧动力灵活配置混合型证券投资基金更新招募说明书（2018年第1号）.txt.zip', 'rb')
    # zip2word.unzip(input_file, result_name)
    # r_list = []  # 外层list是所有的文本list，内层list是一个文本内所有entity的信息
    # for root, dir, files in os.walk(zip2word.UPLOAD_PATH + result_name):
    #     for file in files:
    #         file_name = os.path.join(root, file)
    #         string = word2md.word2string(url, file_name)
    #         r_list.append(main(string))
    # pprint(r_list)
    data = readTxt('20190426_002306_银华合利债券型证券投资基金更新招募说明书（2019年第1号）.txt')
    pprint(main(data))

