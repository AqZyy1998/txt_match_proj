# -*- coding: utf-8 -*-
import os
import zipfile
import shutil
import requests
import app

# 解压zip为word
from flask import request


def unzip(zip_file, zip_filename):
    '''
    解压zip包
    :param zip_file: 二进制方式读取的文件
    :param zip_filename: 去除文件后缀的文件名
    :return: 解压后的文件夹路径，文件夹名
    '''
    pdf_dirpath = os.path.join(UPLOAD_PATH, zip_filename)
    if os.path.isdir(pdf_dirpath):
        shutil.rmtree(pdf_dirpath)
    os.makedirs(pdf_dirpath)
    result_dirpath = os.path.join(RESULT_PATH, zip_filename)
    if os.path.isdir(result_dirpath):
        shutil.rmtree(result_dirpath)
    os.makedirs(result_dirpath)
    zip_filepath = os.path.join(UPLOAD_PATH, zip_filename + '.zip')
    open(zip_filepath, 'wb').write(zip_file.read())
    # zip_file.save(zip_filepath)
    zip_file = zipfile.ZipFile(zip_filepath, 'r')
    zip_file.extractall(pdf_dirpath)

    if os.path.isdir(os.path.join(pdf_dirpath, '__MACOSX')):
        shutil.rmtree(os.path.join(pdf_dirpath, '__MACOSX'))
    for root, dir, files in os.walk(pdf_dirpath):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                filename = file.encode("cp437").decode('utf-8')
            except:
                filename = file.encode('utf-8').decode('utf-8')
            shutil.move(file_path, os.path.join(root, filename))
    return pdf_dirpath, zip_filename

# def unzip(zip_file, zip_filename):
#     '''
#     解压zip包
#     :param zip_file: 二进制方式读取的文件
#     :param zip_filename: 去除文件后缀的文件名
#     :return: 解压后的文件夹路径，文件夹名
#     '''
#     pdf_dirpath = os.path.join(UPLOAD_PATH, zip_filename)
#     if os.path.isdir(pdf_dirpath):
#         shutil.rmtree(pdf_dirpath)
#     os.makedirs(pdf_dirpath)
#     result_dirpath = os.path.join(RESULT_PATH, zip_filename)
#     if os.path.isdir(result_dirpath):
#         shutil.rmtree(result_dirpath)
#     os.makedirs(result_dirpath)
#     zip_filepath = os.path.join(UPLOAD_PATH, zip_filename + '.zip')
#     open(zip_filepath.encode('cp437').decode('gbk'), 'wb').write(zip_file.read())
#     # zip_file.save(zip_filepath)
#     zip_file = zipfile.ZipFile(zip_filepath, 'r')
#     zip_file.extractall(pdf_dirpath)
#     for temp_name in os.listdir(pdf_dirpath):
#         try:
#             new_name = temp_name.encode('cp437').decode('utf-8')
#             os.rename(pdf_dirpath + '/' + temp_name, pdf_dirpath + '/' + new_name)
#         except:
#             pass
#         if os.path.isdir(temp_name):
#             os.chdir(temp_name)
#             os.chdir('..')
#     # print("zip_file: ", zip_file)
#
#     if os.path.isdir(os.path.join(pdf_dirpath, '__MACOSX')):
#         shutil.rmtree(os.path.join(pdf_dirpath, '__MACOSX'))
#
#     return pdf_dirpath, zip_filename


# test
if __name__ == "__main__":
    UPLOAD_PATH = './upload/'
    RESULT_PATH = './result/'

    input_file = open('test.zip', 'rb')

    unzip(input_file, 'test-upload')
