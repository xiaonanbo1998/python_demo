'''
处理设备数据
'''
import urllib
import time
from numpy.lib._iotools import _is_string_like

from base.tool_health_calc import *

import uuid
import numpy

devices = {
    'C0:30:00:23:58:EB': {
        'name': 'blood_pressure',
        'type': 1,
        'id': '176073f7716446e6b67bee1b4332fe1e',
    },
    'C2:18:08:06:31:91': {
        'name': 'glucose',
        'type': 2,
        'id': 'f765658ff33d466d8be9a0f73c9e8beb',
    },
    '84:CC:A8:D5:FC:9E': {
        'name': 'height_weight_bmi',
        'type': 5,
        'id': 'e0024203ad1f4dc8b78b7b97534a0475',
    },
    'C8:A3:EA:02:FE:1D': {
        'name': 'blood_oxgen',
        'type': 3,
        'id': '3c5a416db7f6474f83fd4b0b7220c04a',
    },
    'C0:17:12:01:01:C4': {
        'name': 'heart_beat',
        'type': 4,
        'id': '68c00212f1724484b58a9401d81aae76',
    },
    '00:0E:0B:00:00:97': {
        'name': 'id_card',
        'type': 6,
        'id': '9e85334c35e844a8ae64286c93dc7a1e',
    },
    '00:15:8B:33:25:A3': {
        'name': 'urine',
        'type': 7,
        'id': 'a091665b46e24d11bd88aa26a306adbc',
    },
    'DF:38:8C:B8:9B:67': {
        'name': 'thermometer',
        'type': 8,
        'id': 'b070694b9ade47a9bc21cc97c6210e41'
    },
    'F4:04:4C:10:C9:44': {
        'name': 'uric_acid',
        'type': 9,
        'id': 'ae107d91695746969d0478573844dc6b'
    },
    '2C:AB:33:C3:D3:CE': {
        'name': 'thermometer_paste',
        'type': 10,
        'id': '9108970d18fd48bbb1b1c95d20617514'
    },
}


def parse_connected(d):
    return {
        'id': uuid.uuid1().hex,
        'device_id': devices.get(d.get('mac')).get('id'),
        'type': devices.get(d.get('mac')).get('type'),
        'iscomplete': 0,
        'create_at': int(time.time() * 1000),
    }


def parse_blood_pressure(d):
    '''
    >>> parse_blood_pressure(r4) == {'user_id': 1, 'device_id': '176073f7716446e6b67bee1b4332fe1e', 'type': 1, 'status': '', 'iscomplete': 1, 'vallist': [{'label': '高压', 'val': 110, 'unit': 'mmHg', 'status': 1}, {'label': '低压', 'val': 66, 'unit': 'mmHg', 'status': 1}, {'label': '脉搏', 'val': 83, 'unit': '次/分钟', 'status': 1}]}
    True
    '''
    r = d.get('log')

    if r.get('connected') == 1: return parse_connected(d)

    if not r.get('收缩压'):
        return

    high_pressure = r.get('收缩压')
    low_pressure = r.get('舒张压')
    maibo = r.get('脉搏')

    vallist = [
        {
            "label": "高压",
            "val": high_pressure,
            "unit": "mmHg",
            "status": get_status_ss(high_pressure),
        },
        {
            "label": "低压",
            "val": low_pressure,
            "unit": "mmHg",
            "status": get_status_sz(low_pressure)
        },
        {
            "label": "脉搏",
            "val": maibo,
            "unit": "次/分钟",
            "status": get_status_xl(maibo)
        }
    ]
    return {
        'id': uuid.uuid1().hex,
        #        'user_id':'c58bf33ab49d11ebbe2100d8612d18b0',
        'device_id': devices.get(d.get('mac')).get('id'),
        'type': devices.get(d.get('mac')).get('type'),
        'status': max((get_status_sz(high_pressure), get_status_ss(low_pressure), get_status_xl(maibo))),
        'iscomplete': 1,
        'create_at': int(time.time() * 1000),
        'vallist': vallist,
        'tagname': '',
        'remark': '',
        'score': (cacl_bp_sz(low_pressure) + cacl_bp_ss(high_pressure)) / 2,
    }


def parse_glucose(d):
    '''
    >>> parse_glucose(r5) == {'user_id': 1, 'device_id': 'f765658ff33d466d8be9a0f73c9e8beb', 'type': 2, 'status': '', 'iscomplete': 1, 'vallist': 0.6}
    True
    '''
    r = d.get('log')

    if r.get('connected') == 1: return parse_connected(d)

    if not r.get('血糖值'):
        return

    gv = round(r['血糖值'], 1)

    return {
        'id': uuid.uuid1().hex,
        'user_id': 'c58bf33ab49d11ebbe2100d8612d18b0',
        'device_id': devices.get(d.get('mac')).get('id'),
        'type': devices.get(d.get('mac')).get('type'),
        'status': get_status_xt(gv),
        'iscomplete': 1,
        'create_at': int(time.time() * 1000),
        'tagname': '',
        'remark': '',
        'vallist': [
            {
                "label": "血糖",
                "val": gv,
                "unit": "mmol/L",
                "status": get_status_xt(gv)
            }
        ],
        'score': cacl_bp_xt(gv),
    }


def parse_height_weight_bmi(d):
    '''
    >>> parse_height_weight_bmi(r6_2)

    >>> parse_height_weight_bmi(r6) == {'user_id': 1, 'device_id': 'e0024203ad1f4dc8b78b7b97534a0475', 'type': 5, 'status': '', 'iscomplete': 1, 'vallist': [{'label': '身高', 'val': 1.695, 'unit': 'cm', 'status': 1}, {'label': '体重', 'val': 54.6, 'unit': 'kg', 'status': 1}, {'label': 'BMI', 'val': 19.00435951653745, 'unit': '', 'status': 1}]}
    True
    '''
    r = d.get('log')
    if r.get('iscomplete') not in (0, 1):
        return
    #    if r.get('type') != '结果':
    #        return
    weight = r['weight'] / 100
    height = (r.get('height', numpy.nan) or numpy.nan) / 1000  # r['height'] / 1000
    BMI = round(weight / (height ** 2), 2)
    vallist = [
        {
            "label": "身高",
            "val": height * 100,
            "unit": "cm",
            "status": 1
        },
        {
            "label": "体重",
            "val": weight,
            "unit": "kg",
            "status": 1
        },
        {
            "label": "BMI",
            "val": BMI,
            "unit": "",
            "status": get_status_bmi(height, weight)
        }
    ]
    return {
        'id': uuid.uuid1().hex,
        'user_id': 'c58bf33ab49d11ebbe2100d8612d18b0',
        'device_id': devices.get(d.get('mac')).get('id'),
        'type': devices.get(d.get('mac')).get('type'),
        'status': get_status_bmi(height, weight),
        'iscomplete': r.get('iscomplete'),
        'create_at': int(time.time() * 1000),
        'vallist': vallist,
        'tagname': '',
        'remark': '',
        'score': calc_bmi_score(height, weight),

    }


def parse_blood_oxgen(d):
    '''
    >>> parse_blood_oxgen(r7_2)

    >>> parse_blood_oxgen(r7) == {'user_id': 1, 'device_id': '3c5a416db7f6474f83fd4b0b7220c04a', 'type': 3, 'status': '', 'iscomplete': 1, 'vallist': [{'label': '血氧', 'val': 99, 'unit': '%', 'status': 1}, {'label': '脉率', 'val': 87, 'unit': '次/分钟', 'status': 1}]}
    True
    '''
    r = d.get('log')

    if r.get('connected') == 1: return parse_connected(d)

    if r.get('type') in ('血氧波形包',):
        return

    if not r.get('data') or '脉率分析结果' not in r.get('data').keys():
        return

    # {'data': {'mode': '点测', 'step': '脉率分析', '脉率分析结果': '脉搏节律未见异常'},

    xueo2 = r.get('data')['血氧数据']
    mailv = r.get('data')['脉率数据']
    vallist = [
        {
            "label": "血氧",
            "val": xueo2,
            "unit": "%",
            "status": 1
        },
        {
            "label": "脉率",
            "val": mailv,
            "unit": "bpm",
            "status": 1
        },
        {
            "label": "灌注指数",
            "val": r.get('data').get('血流灌注指数'),
            "unit": "%",
            "status": 1
        }
    ]
    return {
        'id': uuid.uuid1().hex,
        'user_id': 'c58bf33ab49d11ebbe2100d8612d18b0',
        'device_id': devices.get(d.get('mac')).get('id'),
        'type': devices.get(d.get('mac')).get('type'),
        'status': get_status_xy(xueo2 / 100),
        'create_at': int(time.time() * 1000),
        'iscomplete': 1,
        'vallist': vallist,
        'tagname': '',
        'remark': '',
        'score': cacl_bp_xy(xueo2),

    }


def parse_heart_beat(d):
    '''
    >>> parse_heart_beat(r2, 1)

    >>> parse_heart_beat(r3, 1) == {'user_id': 1, 'device_id': '68c00212f1724484b58a9401d81aae76', 'type': 4, 'status': 0, 'iscomplete': 1, 'vallist': '', 'charts': ''}
    True
    '''
    r = d.get('log')

    if r.get('connected') == 1: return parse_connected(d)

    ecg_type = d.get('log').get('ecg_type')

    if ecg_type != '测量结果':
        return
    if d.get('log').get('result')['result'] == 'NML 正常':
        status = 1
        score = 100
    else:
        status = 2
        score = 75
    return {
        'id': uuid.uuid1().hex,
        'user_id': 'c58bf33ab49d11ebbe2100d8612d18b0',
        'device_id': devices.get(d.get('mac')).get('id'),
        'type': devices.get(d.get('mac')).get('type'),
        'status': status,
        'iscomplete': 1,
        'create_at': int(time.time() * 1000),
        'vallist': [],
        'charts': d.get('log').get('waves'),
        'tagname': '',
        'remark': '',
        'score': score,
    }


def parse_id_card(d):
    '''
    >>> parse_id_card(r1, 1) == {'name': '郭森', 'cid': '410526198310220038', 'gender': 1, 'age': 0}
    True
    '''
    r = d.get('log')

    if not r.get('name'):
        return

    return {
        'id': uuid.uuid1().hex,
        'user_id': 'c58bf33ab49d11ebbe2100d8612d18b0',
        'device_id': devices.get(d.get('mac')).get('id'),
        'type': devices.get(d.get('mac')).get('type'),
        'create_at': int(time.time() * 1000),
        'iscomplete': 1,
        'tagname': '',
        'remark': '',
        'vallist': [
            {
                'name': r['name'],
                'cid': r['id'],
                'avatar': r.get('img'),
                'gender': {'男': 1, '女': 2}.get(r['sex'], 0),
            }
        ],
    }


def parse_urine(d):
    '''
    part of ut
    '''

    r = d.get('log')
    # disconnected, return uncompleted data
    if r.get('connected') == 1: return parse_connected(d)
    if r.get('disconnected'): return

    urine_status = get_status_ny(r)
    overall_status = 1 if urine_status['score'] > 80 else 2

    result_data = {
        'id': uuid.uuid1().hex,
        'user_id': 'c58bf33ab49d11ebbe2100d8612d18b0',
        'device_id': devices.get(d.get('mac')).get('id'),
        'type': devices.get(d.get('mac')).get('type'),
        'status': overall_status,
        'iscomplete': 1,
        'create_at': int(time.time() * 1000),
        'vallist': get_vallist(r, urine_status),
        'tagname': '',
        'remark': '',
        'score': urine_status['score'],
    }
    # print('result_data: {}'.format(result_data))

    return result_data


# get urine's vallist
def get_vallist(r, urine_status):
    vallist = [
                {
                    "label": "白细胞",
                    "val": r["白细胞"],
                    "unit": "Cells/μl",
                    "status": urine_status['白细胞']
                },
                {
                    "label": "亚硝酸盐",
                    "val": r["亚硝酸盐"],
                    "unit": "",
                    "status": urine_status['亚硝酸盐']
                },
                {
                    "label": "尿胆原",
                    "val": r["尿胆原"],
                    "unit": "μmol/l",
                    "status": urine_status['尿胆原']
                },
                {
                    "label": "蛋白质",
                    "val": r["蛋白质"],
                    "unit": "g/l",
                    "status": urine_status['蛋白质']
                },
                {
                    "label": "pH值",
                    "val": r["pH值"],
                    "unit": "",
                    "status": urine_status['pH值']
                },
                {
                    "label": "潜血",
                    "val": r["潜血"],
                    "unit": "Cells/μl",
                    "status": urine_status['潜血']
                },
                {
                    "label": "比重",
                    "val": r["比重"],
                    "unit": "",
                    "status": urine_status['比重']
                },
                {
                    "label": "胴体",
                    "val": r["胴体"],
                    "unit": "mmol/l",
                    "status": urine_status['胴体']
                },
                {
                    "label": "胆红素",
                    "val": r["胆红素"],
                    "unit": "μmol/l",
                    "status": urine_status['胆红素']
                },
                {
                    "label": "葡萄糖",
                    "val": r["葡萄糖"],
                    "unit": "mmol/l",
                    "status": urine_status['葡萄糖']
                },
                {
                    "label": "维生素C",
                    "val": r["维生素C"],
                    "unit": "mmol/l",
                    "status": urine_status['维生素C']
                },
                {
                    "label": "微量白蛋白",
                    "val": r["微量白蛋白"],
                    "unit": "mg/l",
                    "status": urine_status['微量白蛋白']
                },
                {
                    "label": "肌酐",
                    "val": r["肌酐"],
                    "unit": "mmol/l",
                    "status": urine_status['肌酐']
                },
                {
                    "label": "钙离子",
                    "val": r["钙离子"],
                    "unit": "mmol/l",
                    "status": urine_status['钙离子']
                }
    ]

    return vallist


def parse_thermometer(d):
    r = d.get('log')
    if r.get('connected') == 1: return parse_connected(d)
    if r.get('disconnected') or r.get('data') is None: return

    if r.get('data') > 37.5:
        print('体温过高，异常...')
        score = 50
    elif r.get('data') > 36.0:
        print('体温正常...')
        score = 100
    else:
        print('体温过低，异常...')
        score = 60

    result_data = {
        'id': uuid.uuid1().hex,
        'user_id': 'c58bf33ab49d11ebbe2100d8612d18b0',
        'device_id': devices.get(d.get('mac')).get('id'),
        'type': devices.get(d.get('mac')).get('type'),
        'status': get_status_tw(r.get('data')),
        'iscomplete': 1,
        'create_at': int(time.time() * 1000),
        'vallist': [
            {
                "label": "体温",
                "val": r.get('data'),
                "unit": "℃",
                "status": get_status_tw(r.get('data')),
            }
        ],
        'tagname': '',
        'remark': '',
        'score': score,
    }
    return result_data


def parse_uric_acid(d):
    r = d.get('log')
    if r.get('connected') == 1: return parse_connected(d)
    if r.get('disconnected'): return

    # 4100葡萄糖，5100尿酸，6100总胆固醇
    if r.get('sequence number') == '4100':
        label = '葡萄糖'
    elif r.get('sequence number') == '5100':
        label = '尿酸'
    elif r.get('sequence number') == '6100':
        label = '总胆固醇'
    else:
        label = '错误类型'

    status = get_status_uricacid(r)
    score = 100 if status == 1 else 60

    result_data = {
        'id': uuid.uuid1().hex,
        'user_id': 'c58bf33ab49d11ebbe2100d8612d18b0',
        'device_id': devices.get(d.get('mac')).get('id'),
        'type': devices.get(d.get('mac')).get('type'),
        'status': status,
        'iscomplete': 1,
        'create_at': int(time.time() * 1000),
        'vallist': [
            {
                "label": label,
                "val": r.get('concentration'),
                "unit": "mmol/L",
                "status": status,
            }
        ],
        'tagname': '',
        'remark': '',
        'score': score,
    }
    return result_data


def parse_thermometer_paste(d):
    r = d.get('log')
    if r.get('connected') == 1: return parse_connected(d)
    if r.get('disconnected') or r.get('data') is None: return

    if r.get('data') > 37.5:
        # print('体温过高，异常...')
        score = 50
    elif r.get('data') > 36.0:
        # print('体温正常...')
        score = 100
    else:
        # print('体温过低，异常...')
        score = 60

    result_data = {
        'id': uuid.uuid1().hex,
        'user_id': 'c58bf33ab49d11ebbe2100d8612d18b0',
        'device_id': devices.get(d.get('mac')).get('id'),
        'type': devices.get(d.get('mac')).get('type'),
        'status': get_status_twt(r.get('data')),
        'iscomplete': 1,
        'create_at': int(time.time() * 1000),
        'vallist': [
            {
                "label": '持续体温',
                "val": r.get('data'),
                "unit": "℃",
                "status": get_status_twt(r.get('data')),
            }
        ],
        'tagname': '',
        'remark': '',
        'score': score,
    }
    return result_data


def get_type(mac):
    return devices.get(mac).get('type')


def get_method_name(mac):
    # print('get_method_name:', 'parse_' + devices.get(mac).get('name'))
    return 'parse_' + devices.get(mac).get('name')


def get_record(d):
    return parsers.get(get_method_name(d.get('mac')))(d)


# parsers means some functions, like 'parse_id_card(d)'...
parsers = {k: v for k, v in locals().items() if k.startswith('parse_')}


def get_url(sys, name, sub=None, uids=None, data={}, id_is_uuid=1, url_prefix='http://localhost:8000/'):
    sub = sub + '/' if sub else ''
    api = 'api'
    #     url = '{api}/{sys}/{sub}{name}s/' if not uids else '{api}/{sys}/{sub}{name}/{uids}/'
    url = '{api}/{sys}/{sub}{name}s/' if not uids else '{api}/{sys}/{sub}{name}/{uids}/'
    uids = ','.join(uids) if uids and not _is_string_like(uids) else uids
    url = url_prefix + url.format(**locals())

    data['id_is_uuid'] = id_is_uuid
    url = '%s?%s' % (url, urllib.parse.urlencode(data))
    return url


import requests

HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}


def test_run():
    sys = 'devcon'
    sub = 'wlp'
    name = 'healthdata'
    url = get_url(sys, name, sub, url_prefix='http://192.168.0.111:8005/')
    print(url, '*' * 10)
    data = pandas.read_csv('../ut_001.csv').to_dict('records')
    for i in range(len(data)):
        r = copy.copy(data[i])
        r['log'] = eval(r.get('log'))
        print(i, r)
        d = get_record(r)
        if d:
            print('#' * 10, d)
            input(">>>")
            requests.request("post", url, json=d, headers=HEADERS)


def test_post():
    # sys = 'devcon'
    # sub = 'wlp'
    # name = 'healthdata'
    # url = get_url(sys, name, sub, url_prefix='http://192.168.0.111:8005/')
    import pandas
    url = 'http://localhost:8000/users/postlog'
    print(url, '*' * 10)
    data = pandas.read_csv('../ut_001.csv').to_dict('records')
    for i in range(len(data)):
        r = copy.copy(data[i])
        r['log'] = eval(r.get('log'))
        print(i, r)
        d = get_record(r)
        if d:
            print('#' * 10, d)
            input(">>>")
            requests.request("post", url, json=d, headers=HEADERS)


if __name__ == '__main__':
    import doctest
    import pandas
    import copy

    data = pandas.read_csv('../ut_001.csv').to_dict('records')


    def get_test_record(i):
        r = copy.copy(data[i])
        r['log'] = eval(r.get('log'))
        return r


    # 身份证
    r1 = get_test_record(4)
    # 心电中间数据
    r2 = get_test_record(31)
    # 心电结果数据
    r3 = get_test_record(303)
    # 血压
    r4 = get_test_record(313)
    # 血糖
    r5 = get_test_record(305)
    # 身高体重bmi结果数据
    r6 = get_test_record(326)
    # 身高体重bmi中间数据
    r6_2 = get_test_record(325)
    # 血氧结果
    r7 = get_test_record(25)
    # 血氧中间数据
    r7_2 = get_test_record(24)
    # print(doctest.testmod(verbose=False, report=False))
    # print(parse_blood_pressure(r4, 1))
    # print(get_record(r1))
    # print(r1)
    # test_run()
    test_post()


