import configparser

def load_config():
    # 加载配置文件
    config = configparser.ConfigParser()
    config.read('options.config', encoding='utf-8')
    return config
