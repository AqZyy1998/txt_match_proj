# -*- coding: UTF-8 -*-
import requests
import json
import word2md
import pprint

def str2list(string):
    url = "http://172.27.231.11:31898"
    payload = {"data": [string]}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    r_list = json.loads(response.text)
    # print("r_list,", r_list)
    entity_list = []
    header_file = open('entitySchemas.json', 'r').read()
    header_json = json.loads(header_file)
    for j in header_json['entitySchemas']:
        tmp = {'entity_type': '', 'entity': ''}
        for i in r_list[0]['entity_list']:
            if i['entity_type'] == str(j['schemaId']) and tmp['entity'] == '':
                tmp['entity_type'] = j['entityType']
                tmp['entity'] = i['entity']
            # 存在同一个entity_type对应多个entity的情况
            elif i['entity_type'] == str(j['schemaId']) and tmp['entity'] != '':
                tmp['entity'] += (';' + i['entity'])
        if tmp['entity'] != '':
            entity_list.append(tmp)
    return entity_list


if __name__ == "__main__":
    word2md.url = "http://172.27.128.117:5022/api/word2md"
    filename = 'upload/line1/20180210_180029_银华永泰积极债券型证券投资基金更新招募说明书（2018年第1号）.doc'
    string = word2md.word2string(word2md.url, filename)
    string = str2list(string)
    print(string)

