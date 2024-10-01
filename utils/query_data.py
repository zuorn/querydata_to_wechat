import os

import pandas as pd
from sqlalchemy import create_engine


# 查询数据代码封装


def query_database(config, task_name):
    if config is None:
        print("配置文件读取失败，数据库查询失败。")
        return None

    # 读取数据库配置
    db_name = config[task_name]['db']
    database_config = config[db_name]

    engine = create_engine(
        f"mysql+pymysql://{database_config['user']}:{database_config['password']}@{database_config['host']}/{database_config['database']}")

    sql_path = config[task_name]['sql']

    with open(sql_path, 'r', encoding='utf-8') as file:
        sql = file.read()
    # params = {'user_json : 182'}
    df = pd.read_sql(sql, engine)
    print("数据库查询成功。")
    return df


# 导出到Exceloutput目录
def export_to_excel(df, config, task_name):
    if df is None:
        print("数据库查询结果为空，Excel文件导出失败。")
        return None
    # 指定导出目录
    output_directory = 'output'

    # 确保目录存在，如果不存在则创建
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # 构建完整的文件路径
    file_name = os.path.join(output_directory, config[task_name]['name'] + '.xlsx')

    # 如果文件已存在，先删除
    if os.path.exists(file_name):
        os.remove(file_name)

    df.to_excel(file_name, index=False)
    print(f"Excel文件： {file_name} 导出成功。")
    return file_name
