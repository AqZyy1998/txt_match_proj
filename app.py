# -*- coding: utf-8 -*-
import traceback

from flask import jsonify, Flask, request, render_template, send_from_directory
import time
import os
import sys
import textMatch, list2csv

app = Flask(__name__)
UPLOAD_FOLDER = 'upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['zip'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[-1] in ALLOWED_EXTENSIONS


# 用于测试上传，稍后用到
@app.route('/')
def upload_test():
    return render_template('upload.html')


@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        zip_filename = f.filename.split('.')[0]
        try:
            list2csv.zip2csv(f, zip_filename, zip_filename + '.csv')
            return send_from_directory('result', zip_filename + '.csv', as_attachment=True)  # 下载文件
        except:  # 异常捕获，打印到日志中
            error = traceback.format_exc().split('\n')  # 返回异常所在位置，字符串形式，不保存到文件
            print(error)
            return jsonify({"errno": 1001, "errmsg": "上传成功，下载失败"})
    else:
        return jsonify({"errno": 1002, "errmsg": "上传失败"})


# 请输入ip和端口号
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5001")
