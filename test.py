import yaml
from sqlalchemy import create_engine, text
import pandas as pd
from utils.read_config import config
from utils.Wechat import send_wechat_msg, upload_file



# 读取配置文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)


def query_data(database_config, sql_path):


    engine = create_engine(
        f"mysql+pymysql://{database_config['user']}:{database_config['password']}@{database_config['host']}/{database_config['database']}")

    with open(sql_path, 'r', encoding='utf-8') as file:
        sql = file.read()
    df = pd.read_sql(sql, engine)
    # print("数据库查询成功。")
    # log.info("数据库查询成功。")
    return df



def test():
    task = config['task1']
    db_config = config[task['db']]
    all_messages = []

    for query in task['queries']:
        sql_path = query['sql_file']
        description = query['description']
        df = query_data(db_config, sql_path)
        message = f"{description} 共有 {len(df)} 条数据。"
        all_messages.append(message)
    return "\n".join(all_messages)

def sen_msg():
    try:
        queries_messages = "sdfsd"
        send_wechat_msg(key=config["task1"]['Robot'], information=queries_messages)
    except Exception as e:
        print(f"发送微信消息失败: {e}")

if __name__ == '__main__':
    sen_msg()

