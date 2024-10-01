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





# 发送微信通知
def send_file(task_name):
    file_path = config[task_name]['export_data']
    name = config[task_name]['name']
    if file_path is None:
        print("找不到Excel文件，文件发送失败。")
        return None
    upload_file(key=config['weixin']['RoBot_key'], path=file_path)
    
    time.sleep(0.5)  # 等待0.5秒,确保文件上传成功后再发送微信通知
    
    send_wechat_msg(key=config['weixin']['RoBot_key'], information=f"✅{name}数据已导出，请查收！")
    print("文件和通知发送成功。")



if __name__ == "__main__":
    config = read_config()

    task_name = config['task_config']['task_name']

    if config is None:
        print("配置文件读取失败，程序退出。")
    else:

           
        df = query_database(config, task_name)
        file_name = export_to_excel(df, config, task_name)
        send_file(task_name)


