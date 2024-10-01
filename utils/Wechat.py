import requests


# 企微机器人代码封装


# 发送消息
def send_wechat_msg(
        key: str = '',
        information: str = '当前未指定微信消息'
):  # 发送微信消息
    """
    发送微信消息
    :type information: str
    :param key: 机器人webhookurl中的key参数
    :param information: 你要发送的消息内容
    """
    try:
        url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'
        mheader = {'Content-Type': 'application/json; charset=UTF-8'}
        mbody = {
            "msgtype": "text",
            "text": {
                "content": information
            }
        }
        # 注意：json=mBody  必须用json
        response = requests.post(url=url, json=mbody, headers=mheader)
        json_res = response.json()  # 返回转为json
        print(f"微信发送成功:\n{information}" if json_res['errcode'] == 0 else
              f"发送失败,参数错误:{json_res['errcode']}\n详情查询:{json_res['errmsg'].split(',')[3][14:]}")
    except Exception as e:
        print("发送微信失败:", e)


# 上传文件
def upload_file(
        key: str = '',
        path: str = ''
):  # 上传文件类型：语音(voice)和普通文件(file)
    """
    上传文件
    :param key: 机器人webhookurl中的key参数
    :param path: 需要上传文件的路径,文件大小不超过20M
    :return:返回请求状态
    """
    try:
        id_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file'  # 上传文件接口地址
        data = {'file': open(path, 'rb')}  # post jason
        response = requests.post(url=id_url, files=data)  # post 请求上传文件
        json_res = response.json()  # 返回转为json
        media_id = json_res['media_id']  # 提取返回ID
        wx_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'  # 发送消息接口地址
        data = {"msgtype": "file", "file": {"media_id": media_id}}  # post json
        r = requests.post(url=wx_url, json=data)  # post请求消息
        print("文件上传成功" if r.status_code == 200 else "上传错误")
        return r  # 返回请求状态
    except Exception as e:
        print("文件发送失败:", e)
