## 山东理工大学体测预约脚本
```angular2html
 ____   ____   _   _  _____            _     ____   ____    ___   ___  _   _  _____  __  __  _____  _   _  _____ 
/ ___| |  _ \ | | | ||_   _|          / \   |  _ \ |  _ \  / _ \ |_ _|| \ | ||_   _||  \/  || ____|| \ | ||_   _|
\___ \ | | | || | | |  | |   _____   / _ \  | |_) || |_) || | | | | | |  \| |  | |  | |\/| ||  _|  |  \| |  | |  
 ___) || |_| || |_| |  | |  |_____| / ___ \ |  __/ |  __/ | |_| | | | | |\  |  | |  | |  | || |___ | |\  |  | |  
|____/ |____/  \___/   |_|         /_/   \_\|_|    |_|     \___/ |___||_| \_|  |_|  |_|  |_||_____||_| \_|  |_| 
```
### 概述
- 【初衷】：帮助SDUT体测预约的同学们把盯预约的时间做其他更有意义的事情
- 【技术栈】：基于网页自动化工具库[drissionpage](https://github.com/g1879/DrissionPage)
### 功能
- [x] 自动登录
- [x] 多种预约模式
- [x] 多线程预约
- [x] 支持浏览器模拟点击
- [x] 支持接口直发
### 使用简介
填写[`options.config`](./options.config)文件，运行[main.py](./main.py)即可，或者使用[exc.bat]()

### 支持的浏览器
| 浏览器 | 版本  | 下载链接 |
|--------|-------|----------|
| <img src="https://pic.zjcspace.xyz/b/202411131916861.svg" alt="Chrome" width="32" height="32"> |$$\geq 100.0$$ | [下载 Chrome](https://www.google.com/chrome/) |

### 环境

| 环境                                                                                                    | 版本  |
|-------------------------------------------------------------------------------------------------------|-------|
| <img src="https://pic.zjcspace.xyz/b/202411131920654.svg" alt="Chrome" width="32" height="32"> (开发环境) | 3.8 
| <img src="https://pic.zjcspace.xyz/b/202411131925584.svg" alt="Chrome" width="32" height="32"> (开发环境) | $$\geq 10$$

## 关于接口直发模式
- 打开浏览器，进入登录界面(非认证界面)，F12打开控制台，打开network(网络)抓取数据包
- 输入账号，密码 点击登录，查看`/api/sys/user/bind/wechat`接口的payload数据
- 找到`name`字段， 为加密的密码