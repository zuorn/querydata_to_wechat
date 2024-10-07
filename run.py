import configparser
import time

from utils.Wechat import send_wechat_msg, upload_file
from utils.query_data import query_database, export_to_excel


# 检查配置文件是否正确读取
def read_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini', encoding='utf-8')
        print("配置文件读取成功。")
    except UnicodeDecodeError:
        print("配置文件解码错误。请确保它是UTF-8格式。")
        return None
    return config


# 倒计时函数
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"倒计时: {i} 秒", end="\r")
        time.sleep(1)
    print(seconds, "秒倒计时结束！")


# 发送微信通知
def send_file(task_name, file_path):
    name = config[task_name]['name']
    if file_path is None:
        print(f"找不到Excel文件，文件发送失败。任务名: {task_name}")
        return None

    # 上传文件到企业微信
    rebot = config[task_name]['Robot']
    upload_file(key=config[rebot]['RoBot_key'], path=file_path)

    # time.sleep(2)  # 等待2秒,确保文件上传成功后再发送微信通知
    countdown(2)

    send_wechat_msg(key=config[rebot]['RoBot_key'], information=f"✅{name}数据已导出，请查收！")
    print(f"文件和通知发送成功。任务名: {task_name}")

    # 每个任务执行完成后等待5秒
    # time.sleep(5)
    countdown(5)


#  任务执行函数
def execute_task(task_name):
    if config is None:
        print("配置文件读取失败，程序退出。")
    else:

        df = query_database(config, task_name)
        file_name = export_to_excel(df, config, task_name)
        send_file(task_name, file_name)


# 读取运行的任务
def task_names_to_list():
    task_names = config['task_config']['task_name'].split(',')
    for task_name in task_names:
        execute_task(task_name)
        print(task_name + "执行完成。")
        print("-----------------------------------")
    print("所有任务执行完成。")


if __name__ == "__main__":
    config = read_config()
    if config is None:
        print("配置文件读取失败，程序退出。")
    else:
        task_names_to_list()
