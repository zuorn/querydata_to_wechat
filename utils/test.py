import configparser
import time

import pandas as pd
from sqlalchemy import create_engine


# from utils.logs import log

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


# 查询数据代码封装
def data_select(database_config, sql):
    # 创建数据库引擎
    engine = create_engine(
        f"mysql+pymysql://{database_config['user']}:{database_config['password']}@{database_config['host']}/{database_config['database']}")

    # 执行SQL查询
    # sql = "SELECT * FROM `cloud2.0`.`blade_region`"
    df = pd.read_sql(sql, engine)
    print("数据库查询成功。")
    # log.info("数据库查询成功。")
    return df


def taskk():
    # 读取配置文件
    config = read_config()

    db = config['task1']['db']
    database_config = config[db]
    print(database_config)

    # 指定SQL语句
    sql = "SELECT * FROM `cloud2.0`.`blade_region`"
    df = data_select(database_config, sql)
    print(f"查询结果：{len(df)}")


if __name__ == "__main__":
    config = read_config()
    # countdown(3)
    # query_database(config, 'task1')
    taskk()
