import time
from datetime import datetime

from utils.Wechat import send_wechat_msg, upload_file
from utils.logs import log
from utils.query_data import  export_to_excel, query_data
from utils.read_config import config
from utils.data_processing.exce_processing import exce_processing


# 倒计时函数
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"倒计时: {i} 秒", end="\r")
        log.info(f"倒计时: {i} 秒")
        time.sleep(1)
    print(seconds, "秒倒计时结束！")
    log.info(f"{seconds}秒倒计时结束！")

# Excel 数据处理函数
def data_processing():
    exce_processing()


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



# 查询数据库并返回查询结果，发送微信配置模板通知
def queries(task_name):

    # 读取数据库配置
    db_name = config[task_name]['db']
    database_config = config[db_name]
    
    all_messages = []

    for query in config[task_name]['queries']:
        sql_path = query['sql_file']
        description = query['description']
        df = query_data(database_config, sql_path)
        message = f"{description} 共有 {len(df)} 条数据。"
        all_messages.append(message)
    return "\n".join(all_messages)



# 查询数据库并导出Excel文件发送微信通知
def execute_task_run(task_name):

    # 读取数据库配置
    db_name = config[task_name]['db']
    database_config = config[db_name]

    # 检查是否有queries配置
    if 'queries' in config[task_name]:

        name = config[task_name]['name']
        queries_messages = queries(task_name)
        print(queries_messages)
        log.info(queries_messages.replace("\n", "  "))

        # 发送微信通知
        rebot = config[task_name]['Robot']
        send_wechat_msg(key=config[rebot]['RoBot_key'], information=f"{queries_messages}\n✅{name}数据已导出，请查收！")



    else:
        sql = config[task_name]['sql']
        if sql is None:
            print(f"任务{task_name}没有指定查询SQL，跳过执行。")
            return

        df = query_data(database_config, sql)
        file_name = export_to_excel(df, config, task_name)
        exce_processing(file_name)
        send_file(task_name, file_name)




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
            current_date = datetime.now().date()

            # 确保 end_date 是 datetime.date 对象
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()  # 将字符串转换为日期对象

            # 如果截止日期大于等于当前日期，执行任务
            if end_date >= current_date:
                print(f"任务{task_name}在截止日期{end_date}之前，开始执行。")
                log.info(f"任务{task_name}在截止日期{end_date}之前，开始执行。")
                execute_task_run(task_name)

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
                execute_task_run(task_name)
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
