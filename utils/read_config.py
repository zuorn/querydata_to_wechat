import configparser

from utils.logs import log


# 检查配置文件是否正确读取
def read_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini', encoding='utf-8')
        print("配置文件读取成功。")
        log.info("配置文件读取成功。")
    except UnicodeDecodeError:
        print("配置文件解码错误。请确保它是UTF-8格式。")
        log.error("配置文件解码错误。请确保它是UTF-8格式。")
        return None
    return config


# 读取配置文件
config = read_config()
