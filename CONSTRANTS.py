# sdut认证url

HOST = 'http://tcenter.sdut.edu.cn/'

AUTH_URL = 'http://10-17-27-11.newvpn.sdut.edu.cn:8118/'

AUTH_LOGOUT_URL = 'https://newvpn.sdut.edu.cn/passport/v1/user/logout?clientType=SDPBrowserClient&platform=Windows&lang=zh-CN'

NOTICE_URL = HOST+'/api/interinfo/notice/toList?sf_request_type=ajax'

INNER_URL = HOST+'/#/test/1'
OUTER_URL = HOST+'/#/test/2'

AP_LIST = "/api/tzjc/testappointment/get-appointment-date-list"

APP_DATE_LIST = HOST+'/api/tzjc/testappointment/get-appointment-time-list?sf_request_type=ajax'
APP_TIME_PERIOD = HOST+'/api/tzjc/testappointment/get-appointment-time-type?sf_request_type=ajax'
AP_APPLY = HOST+'/api/tzjc/testappointment/apply?sf_request_type=ajax'
APP_LIST = HOST+'/api/tzjc/testappointment/get-appointment-date-list?sf_request_type=ajax'
AP_LOGIN = HOST+'/api/sys/user/bind/wechat?sf_request_type=ajax'
WARN1 = '距离上次预约时间未超50天，无法继续预约，如有疑问，请联系相关老师!'



cookies = {
    # 'platformMultilingual_-_edu.cn': 'zh_CN',
    # 'sdp_user_token': '',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
    # 'Cookie': 'platformMultilingual_-_edu.cn=zh_CN; sdp_user_token=4a07fdd7-cc46-4c9d-a037-e005599422a2_dabfa38a-c70e-4610-9a56-d656b106d932',
    'Origin': HOST,
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': HOST,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

params = {
    'sf_request_type': 'ajax',
}

