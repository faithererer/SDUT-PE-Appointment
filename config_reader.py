import configparser


def load_config():
    # 加载配置文件
    config = configparser.ConfigParser()
    config.read('options.config', encoding='utf-8')
    return config


def get_mode():
    # 加载配置文件
    config = configparser.ConfigParser()
    config.read('options.config', encoding='utf-8')
    return config.get('DEFAULT', 'mode')

def get_policy():
    # 加载配置文件
    config = configparser.ConfigParser()
    config.read('options.config', encoding='utf-8')
    return config.get('DEFAULT', 'policy')

def get_skip():
    # 加载配置文件
    config = configparser.ConfigParser()
    config.read('options.config', encoding='utf-8')
    return config.get('DEFAULT', 'skip')