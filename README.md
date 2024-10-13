# 执行数据库查询并将结果导出为Excel发送微信群

## 前言

本项目是一个Python脚本，用于执行数据库查询并将结果发送微信通知。

### 实现功能

- 执行数据库查询
- 将查询结果导出为Excel文件
- 将Excel文件发送到企业微信群
- 可配置多个任务同时执行
- 任务可配置不同的数据库
- 任务可配置不同的企业微信机器人，分别发送到不同的企业微信群
- 任务可配置模板统计文本并指定对应数据库查询语句
- 任务配置截止日期：如果截止日期大于等于当前日期，执行任务
- 任务配置执行日期：如果当前日期在执行日期列表中，执行任务
- 完整的日志记录

### 目录结构

```
├── config.ini   # 配置文件
├── run.py       # 主程序
├── utils
│   ├── execute_task.py # 执行任务封装
│   ├── wechat.py       # 企业微信封装
│   └── query_data.py   # 数据库查询封装
│   └── read_config.py  # 读取配置文件封装
│   └── logs.py         # 日志封装
├── logs
│   ├── 2024-10-09.log  # 日志文件
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
2024-10-11 21:13:47,680 - TaskExecution - INFO - 配置文件读取成功。
2024-10-11 21:13:48,059 - TaskExecution - INFO - 开始执行任务: ['task1', 'task2', 'task3']
2024-10-11 21:13:48,059 - TaskExecution - INFO - -----------------------------------
2024-10-11 21:13:48,059 - TaskExecution - INFO - 任务task1在执行日期2024-10-11，开始执行。
2024-10-11 21:13:48,211 - TaskExecution - INFO - 数据库查询成功。
2024-10-11 21:13:48,683 - TaskExecution - INFO - 导出Excel文件： output\任务1.xlsx 成功。
2024-10-11 21:13:52,986 - TaskExecution - INFO - 倒计时: 2 秒
2024-10-11 21:13:53,998 - TaskExecution - INFO - 倒计时: 1 秒
2024-10-11 21:13:55,002 - TaskExecution - INFO - 2秒倒计时结束！
2024-10-11 21:13:55,239 - TaskExecution - INFO - 微信发送成功:✅任务1数据已导出，请查收！
2024-10-11 21:13:55,240 - TaskExecution - INFO - 文件和通知发送成功。任务名: task1
2024-10-11 21:13:55,240 - TaskExecution - INFO - 倒计时: 5 秒
2024-10-11 21:13:56,240 - TaskExecution - INFO - 倒计时: 4 秒
2024-10-11 21:13:57,249 - TaskExecution - INFO - 倒计时: 3 秒
2024-10-11 21:13:58,250 - TaskExecution - INFO - 倒计时: 2 秒
2024-10-11 21:13:59,255 - TaskExecution - INFO - 倒计时: 1 秒
2024-10-11 21:14:00,256 - TaskExecution - INFO - 5秒倒计时结束！
2024-10-11 21:14:00,257 - TaskExecution - INFO - task1执行完成。
2024-10-11 21:14:00,257 - TaskExecution - INFO - -----------------------------------
2024-10-11 21:14:00,257 - TaskExecution - INFO - 任务task2在截止日期2024-10-13之前，开始执行。
2024-10-11 21:14:00,263 - TaskExecution - INFO - 数据库查询成功。
2024-10-11 21:14:00,286 - TaskExecution - INFO - 导出Excel文件： output\任务2.xlsx 成功。
2024-10-11 21:14:00,941 - TaskExecution - INFO - 倒计时: 2 秒
2024-10-11 21:14:01,949 - TaskExecution - INFO - 倒计时: 1 秒
2024-10-11 21:14:02,959 - TaskExecution - INFO - 2秒倒计时结束！
2024-10-11 21:14:03,197 - TaskExecution - INFO - 微信发送成功:✅任务2数据已导出，请查收！
2024-10-11 21:14:03,197 - TaskExecution - INFO - 文件和通知发送成功。任务名: task2
2024-10-11 21:14:03,197 - TaskExecution - INFO - 倒计时: 5 秒
2024-10-11 21:14:04,210 - TaskExecution - INFO - 倒计时: 4 秒
2024-10-11 21:14:05,213 - TaskExecution - INFO - 倒计时: 3 秒
2024-10-11 21:14:06,228 - TaskExecution - INFO - 倒计时: 2 秒
2024-10-11 21:14:07,243 - TaskExecution - INFO - 倒计时: 1 秒
2024-10-11 21:14:08,254 - TaskExecution - INFO - 5秒倒计时结束！
2024-10-11 21:14:08,256 - TaskExecution - INFO - task2执行完成。
2024-10-11 21:14:08,256 - TaskExecution - INFO - -----------------------------------
2024-10-11 21:14:08,256 - TaskExecution - INFO - 任务task3没有指定截止日期或执行日期，跳过执行。
2024-10-11 21:14:08,256 - TaskExecution - INFO - task3执行完成。
2024-10-11 21:14:08,257 - TaskExecution - INFO - -----------------------------------
2024-10-11 21:14:08,258 - TaskExecution - INFO - 共执行3个任务，分别为：['task1', 'task2', 'task3']。

```

## 准备工作

### 添加企微机器人

企业微信群，点击【添加机器人】-【创建一个机器人】-【填写机器人名称】-添加号机器人复制key，并配置在config-RoBot_key

### 让微信也能查看企微群消息

登录企业微信后台后，点击我的企业-微信插件，扫描二维码。这样就以在微信里查看企业微信的群消息啦！

## TODO

### 数据处理

- Excel格式调整
    - 冻结首行
    - 填充首行颜色
    - 设置自适应列宽
    - 设置所有数据单元格框线

## 常见问题

### '%' (0x25) at index 232`

错误：`ValueError: unsupported format character '%' (0x25) at index 232`

处理：sql中包含% 号，需要转义，在% 前加一个% 即可。
