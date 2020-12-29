# coding:utf-8
# 配置服务的日志格式和位置
import logging
from logging import handlers
from app import *

# log
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)  # 日志级别为info
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # 时间戳
file_handler = handlers.TimedRotatingFileHandler(filename=
    os.path.join(app.BASE_DIR,'./log/server_log'), when="D", interval=1, backupCount=7)  # 指定文件及其格式
file_handler.setLevel(level=logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# console
stream_handler = logging.StreamHandler()  # 将日志输出到控制台，通过流传输
stream_handler.setLevel(level=logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)