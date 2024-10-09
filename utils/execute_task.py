import time

from utils.Wechat import send_wechat_msg, upload_file
from utils.logs import log
from utils.query_data import query_database, export_to_excel
from utils.read_config import config


# 倒计时函数
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"倒计时: {i} 秒", end="\r")
        log.info(f"倒计时: {i} 秒")
        time.sleep(1)
    print(seconds, "秒倒计时结束！")
    log.info(f"{seconds}秒倒计时结束！")


# 发送微信通知
def send_file(task_name, file_path):
    name = config[task_name]['name']
    if file_path is None:
        print(f"找不到Excel文件，文件发送失败。任务名: {task_name}")
        log.error(f"找不到Excel文件，文件发送失败。任务名: {task_name}")
        return None

    # 上传文件到企业微信
    rebot = config[task_name]['Robot']
    upload_file(key=config[rebot]['RoBot_key'], path=file_path)

    # 等待2秒,确保文件上传成功后再发送微信通知
    countdown(2)

    send_wechat_msg(key=config[rebot]['RoBot_key'], information=f"✅{name}数据已导出，请查收！")
    print(f"文件和通知发送成功。任务名: {task_name}")
    log.info(f"文件和通知发送成功。任务名: {task_name}")

    # 每个任务执行完成后等待5秒
    countdown(5)


#  任务执行函数
def execute_task(task_name):
    if config is None:
        print("配置文件读取失败，程序退出。")
        log.error("配置文件读取失败，程序退出。")
    else:
        # 读取任务配置的截止日期
        if 'end_date' in config[task_name]:
            end_date = config[task_name]['end_date']
            # 获取当前日期
            current_date = time.strftime("%Y-%m-%d", time.localtime())

            # 如果截止日期大于等于当前日期，执行任务
            if end_date >= current_date:
                print(f"任务{task_name}在截止日期{end_date}之前，开始执行。")
                log.info(f"任务{task_name}在截止日期{end_date}之前，开始执行。")
                df = query_database(config, task_name)
                file_name = export_to_excel(df, config, task_name)
                send_file(task_name, file_name)
            else:
                print(f"任务{task_name}在截止日期{end_date}之后，跳过执行。")
                log.info(f"任务{task_name}在截止日期{end_date}之后，跳过执行。")

        # 读取任务配置的执行日期
        elif 'execution_date' in config[task_name]:
            execution_dates = config[task_name]['execution_date'].split(',')
            current_date = time.strftime("%Y-%m-%d", time.localtime())
            
            # 如果当前日期在执行日期列表中，执行任务
            if current_date in execution_dates:
                print(f"任务{task_name}在执行日期{current_date}，开始执行。")
                log.info(f"任务{task_name}在执行日期{current_date}，开始执行。")
                df = query_database(config, task_name)
                file_name = export_to_excel(df, config, task_name)
                send_file(task_name, file_name)
            else:
                print(f"任务{task_name}不在执行日期{current_date}，跳过执行。")
                log.info(f"任务{task_name}不在执行日期{current_date}，跳过执行。")
        else:
            print(f"任务{task_name}没有指定截止日期或执行日期，跳过执行。")
            log.info(f"任务{task_name}没有指定截止日期或执行日期，跳过执行。")


# 读取运行的任务
def task_names_to_list():
    task_names = config['task_config']['task_name'].split(',')
    print(f"开始执行任务: {task_names}")
    print("-----------------------------------")

    log.info(f"开始执行任务: {task_names}")
    log.info("-----------------------------------")

    for task_name in task_names:
        execute_task(task_name)
        print(task_name + "执行完成。")
        log.info(task_name + "执行完成。")

        print("-----------------------------------")
        log.info("-----------------------------------")
    print(f"共执行{len(task_names)}个任务，分别为：{task_names}。")
    log.info(f"共执行{len(task_names)}个任务，分别为：{task_names}。")
