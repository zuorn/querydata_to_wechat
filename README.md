# 执行数据库查询并将结果导出为Excel发送微信群

## 前言

本项目是一个Python脚本，用于执行数据库查询并将结果导出为Excel文件，然后通过企业微信机器人发送到指定的企业微信群。

### 实现功能

- 执行数据库查询
- 将查询结果导出为Excel文件
- 将Excel文件发送到企业微信群
- 可配置多个任务同时执行
- 每个任务可配置不同的数据库
- 每个任务可配置不同的企业微信机器人，分别发送到不同的企业微信群
- 每个任务可配置不同的截止日期，超过截止日期则跳过执行
- 完整的日志记录，方便排查问题

### 目录结构

```
├── config.ini   # 配置文件
├── run.py       # 主程序
├── utils
│   ├── execute_task.py # 执行任务封装
│   ├── wechat.py       # 企业微信封装
│   └── query_data.py   # 数据库查询封装
│   └── logs.py         # 日志封装
├── logs
│   ├── 2024-10-08.log  # 日志文件
├── sql
│   ├── 任务1.sql        # 任务1的SQL语句
│   ├── 任务2.sql
│   └── 任务3.sql
└── output
    ├── 任务1.xlsx       # 任务1的Excel文件
    ├── 任务2.xlsx
    └── 任务3.xlsx
```

### 安装依赖：

```shell
pip install -r requirements.txt 
```

### 运行：

```shell
python run.py
```

### 执行日志：

```log
2024-10-08 23:17:57,782 - TaskExecution - INFO - 配置文件读取成功。
2024-10-08 23:17:57,782 - TaskExecution - INFO - 开始执行任务: ['task1', 'task2', 'task3']
2024-10-08 23:17:57,782 - TaskExecution - INFO - -----------------------------------
2024-10-08 23:17:57,782 - TaskExecution - INFO - 任务task1在截止日期2024-10-24之前，开始执行。
2024-10-08 23:17:57,857 - TaskExecution - INFO - 数据库查询成功。
2024-10-08 23:17:57,918 - TaskExecution - INFO - 导出Excel文件： output\任务1.xlsx 成功。
2024-10-08 23:17:58,512 - TaskExecution - INFO - 倒计时: 2 秒
2024-10-08 23:17:59,524 - TaskExecution - INFO - 倒计时: 1 秒
2024-10-08 23:18:00,537 - TaskExecution - INFO - 2秒倒计时结束！
2024-10-08 23:18:00,790 - TaskExecution - INFO - 微信发送成功:✅任务1数据已导出，请查收！
2024-10-08 23:18:00,790 - TaskExecution - INFO - 文件和通知发送成功。任务名: task1
2024-10-08 23:18:00,790 - TaskExecution - INFO - 倒计时: 5 秒
2024-10-08 23:18:01,800 - TaskExecution - INFO - 倒计时: 4 秒
2024-10-08 23:18:02,812 - TaskExecution - INFO - 倒计时: 3 秒
2024-10-08 23:18:03,814 - TaskExecution - INFO - 倒计时: 2 秒
2024-10-08 23:18:04,814 - TaskExecution - INFO - 倒计时: 1 秒
2024-10-08 23:18:05,828 - TaskExecution - INFO - 5秒倒计时结束！
2024-10-08 23:18:05,828 - TaskExecution - INFO - task1执行完成。
2024-10-08 23:18:05,828 - TaskExecution - INFO - -----------------------------------
2024-10-08 23:18:05,829 - TaskExecution - INFO - 任务task2在截止日期2024-10-07之后，跳过执行。
2024-10-08 23:18:05,829 - TaskExecution - INFO - task2执行完成。
2024-10-08 23:18:05,829 - TaskExecution - INFO - -----------------------------------
2024-10-08 23:18:05,829 - TaskExecution - INFO - 任务task3在截止日期2024-10-08之前，开始执行。
2024-10-08 23:18:05,837 - TaskExecution - INFO - 数据库查询成功。
2024-10-08 23:18:05,865 - TaskExecution - INFO - 导出Excel文件： output\任务3.xlsx 成功。
2024-10-08 23:18:06,494 - TaskExecution - INFO - 倒计时: 2 秒
2024-10-08 23:18:07,501 - TaskExecution - INFO - 倒计时: 1 秒
2024-10-08 23:18:08,502 - TaskExecution - INFO - 2秒倒计时结束！
2024-10-08 23:18:08,737 - TaskExecution - INFO - 微信发送成功:✅任务3数据已导出，请查收！
2024-10-08 23:18:08,737 - TaskExecution - INFO - 文件和通知发送成功。任务名: task3
2024-10-08 23:18:08,738 - TaskExecution - INFO - 倒计时: 5 秒
2024-10-08 23:18:09,738 - TaskExecution - INFO - 倒计时: 4 秒
2024-10-08 23:18:10,751 - TaskExecution - INFO - 倒计时: 3 秒
2024-10-08 23:18:11,758 - TaskExecution - INFO - 倒计时: 2 秒
2024-10-08 23:18:12,759 - TaskExecution - INFO - 倒计时: 1 秒
2024-10-08 23:18:13,773 - TaskExecution - INFO - 5秒倒计时结束！
2024-10-08 23:18:13,774 - TaskExecution - INFO - task3执行完成。
2024-10-08 23:18:13,775 - TaskExecution - INFO - -----------------------------------
2024-10-08 23:18:13,775 - TaskExecution - INFO - 共执行3个任务，分别为：['task1', 'task2', 'task3']。
```

## 准备工作

### 添加企微机器人

企业微信群，点击【添加机器人】-【创建一个机器人】-【填写机器人名称】-添加号机器人复制key，并配置在config-RoBot_key

### 让微信也能查看企微群消息

登录企业微信后台后，点击我的企业-微信插件，扫描二维码。这样就可以在微信里查看企业微信的群消息啦！
![img_4.png](.img/img_4.png)

## 常见问题

### '%' (0x25) at index 232`

错误：`ValueError: unsupported format character '%' (0x25) at index 232`

处理：sql中包含% 号，需要转义，在% 前加一个% 即可。
