import configparser


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


if __name__ == "__main__":
    config = read_config()
    test()
