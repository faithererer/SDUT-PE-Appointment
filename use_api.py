from random import random

import AppoiintmentType
import json
import threading
import time

import CONSTRANTS
import config_reader
import gbl
import my_logger
from Chrome import Chrome
from appoitment import *
from art import *
import requests
from auth_sdut import logger, auth_sdut, deal_notice, get_sdp_user_token


def check_sorry(s, headers, bs, session):
    if 'Sorry' in s:
        if get_sdp_user_token(bs) not in ['', None]:
            logger.info("已认证")
        else:
            state, page = auth_sdut()
        sdp_user_token = get_sdp_user_token(bs)
        if sdp_user_token is not None:
            logger.info(f"sdp_user_token:\t{sdp_user_token}")
        else:
            logger.error("sdp_user_token为空.获取失败")
            return False
        opts = config_reader.load_config()
        username = opts.get('DEFAULT', 'username')
        password = opts.get('DEFAULT', 'password_encoded')
        logger.info(f"开始登录,你的账号:{username}\t密码(加密):{password}")
        headers['Cookie'] = f'sdp_user_token={sdp_user_token}'
        login_res = session.post(url=CONSTRANTS.AP_LOGIN,
                                 json={"number": username, "name": password},
                                 headers=CONSTRANTS.headers)
        login_json = {}
        try:
            login_json = json.loads(login_res.text)
        except Exception as e:
            logger.error(f"登录信息不是正常信息:{login_res.text}")
            check_sorry(login_res.text, headers, Chrome().get_browser(), session)
            print(headers)
            return False
        if login_json['status'] != 1:
            logger.error(f"登录失败:{login_json['message']}")
        token = login_json["result"]["token"]
        logger.info("登录成功, token:" + token)
        headers['Authorization'] = f'{token}'
        return True


def logined(coo_list):
    i = 0
    for coo in coo_list:
        if coo['domain'] == '.newvpn.sdut.edu.cn' and coo['name'] == 'sdp_user_token' \
                and coo['value'] not in ['', None]:
            i += 1
        if coo['domain'] == '10-17-27-11.newvpn.sdut.edu.cn' and coo['name'] == 'JSESSIONID' \
                and coo['value'] not in ['', None]:
            print(coo)
            i += 1
        if i >= 2:
            return True
    return False


def appointment_by_api(app_type, session, m_th=None, lock=None):
    bs = Chrome().get_browser()
    bs.new_tab("http://10-17-27-11.newvpn.sdut.edu.cn:8118/")
    bs.set.cookies.clear()
    logger.info("正在认证...")
    while True:
        headers = CONSTRANTS.headers
        if m_th is True and lock is not None:
            # 加锁，只允许一个线程执行，不自旋
            with lock:
                while not check_sorry("Sorry", headers, bs, session): pass
        else:
            while not check_sorry("Sorry", headers, bs, session): pass

        logger.warning("开始预约，当前预约类型:" + app_type.name)
        while True:
            logger.info("可用日期")
            from appoitment import get_date_list
            date_list = get_date_list(session, headers, app_type)
            if date_list is None or len(date_list) == 0:
                t = random.randint(3, 5)
                logger.warning(f"当前没有预约信息, {t}秒后重试")
                time.sleep(t)
                continue
            for dt in date_list[::-1]:
                logger.info(f"【{app_type.name}】:{dt}")
                from appoitment import get_app_list_oneday
                app_list = get_app_list_oneday(session, headers, dt, app_type)
                for app in app_list:
                    logger.info(
                        f"【{app_type.name}】预约时间段:{app['dateStart']}-{app['dateEnd']}\t人数:{app['numApply']}/{app['numMax']}")
                    if app['dateStart'] not in ['', None]:
                        if app['numApply'] >= app['numMax']:
                            logger.info(f"人数已满")
                            continue
                        elif "08:00" in app['dateStart']:
                            logger.warning("虽然有空位，但是08:00-09:00太早了，跳过")
                            continue
                        from appoitment import apply
                        apply_res = apply(session, headers, app['id'])
                        logger.info(apply_res)
                        if apply_res['status'] == 1:
                            logger.info(f"预约成功")
                            gbl.result[app_type] = True
                            return True
                        elif apply_res['status'] == -1 and '距离上次预约时间未超' in apply_res['message']:
                            logger.error(f"预约失败:预约时间间隔过短:{apply_res['message']}")
                            gbl.result[app_type] = False
                            return False
                        else:
                            logger.error(f"预约失败:{apply_res['message']}")
                    else:
                        logger.info(f"时间段不可用")
            time.sleep(random.randint(0, 2))
