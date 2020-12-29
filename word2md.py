# -*- coding: UTF-8 -*-
import requests
import re, json, os


def word2string(url, filename):
  print("filename: ", filename.encode('utf-8').decode())
  payload = {}
  files = [
    ('file', open(filename.encode('utf-8').decode(), 'rb'))
  ]
  headers = {}
  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  string = response.text.encode('utf-8').decode('utf-8')
  # try:
  #   string = response.text.encode('cp437').decode('utf-8')
  # except:
  #   string = response.text.encode('utf-8').decode('utf-8')
  return string


# test
if __name__ == "__main__":
  url = "http://172.27.128.117:5022/api/word2md"
  filename = 'upload/d_line1/20201209_000286_银华信用季季红债券型证券投资基金更新招募说明书（2020年第3号）的副本.docx'
  string = word2string(url, filename)
  print(string)
