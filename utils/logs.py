import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 创建 logs 文件夹（如果不存在）
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # 获取当前时间并格式化为字符串
        current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        log_file_name = f'logs/{current_time}.log'

        # 设置文件处理程序，指定编码为 utf-8
        file_handler = logging.FileHandler(log_file_name, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


# 初始话日志对象
log = Logger("TaskExecution")
