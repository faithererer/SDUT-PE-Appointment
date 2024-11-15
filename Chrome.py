import threading

from DrissionPage._base.chromium import Chromium
from DrissionPage._configs.chromium_options import ChromiumOptions


# 单例

class Chrome(object):
    _instance = None
    _lock = threading.Lock()  # 创建一个锁对象

    def get_browser(self):
        with self._lock:  # 使用with语句自动管理锁的获取和释放
            # 创建配置对象（默认从ini文件中读取配置，这里简化处理，不涉及实际ini读取逻辑）
            co = ChromiumOptions()
            # 设置不加载图片、静音等配置选项（具体是否有对应接口需要根据实际使用的库来定，这里以playwright的类似设置思路为例）

            if not Chrome._instance:
                try:
                    Chrome._instance = Chromium(addr_or_opts=co)
                except Exception as e:
                    print(f"创建浏览器实例时出现错误: {e}")
                    # 可以在这里添加重试逻辑或者返回默认的错误提示等操作
        return Chrome._instance
