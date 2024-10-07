import configparser
import time


def read_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini', encoding='utf-8')
        print("配置文件读取成功。")
    except UnicodeDecodeError:
        print("配置文件解码错误。请确保它是UTF-8格式。")
        return None
    return config


def test():
    db_name = config['task']['db']
    print(db_name)

    db_config = config[db_name]

    print(db_config)


def RoBot_key():
    robot = config['task']['Robot']
    print(robot)

    rebot_k = config[robot]['RoBot_key']
    print(rebot_k)


def task_names():
    config = read_config()
    task_names = config['task_config']['task_name'].split(',')
    print(task_names)


# 倒计时函数
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"倒计时: {i} 秒", end="\r")
        time.sleep(1)
    print("倒计时结束！")


if __name__ == "__main__":
    config = read_config()
    countdown(3)
