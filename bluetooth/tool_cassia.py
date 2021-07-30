import json
import pprint
import threading
import time

import requests
from requests.adapters import HTTPAdapter
import sseclient

from base import tool_yy, tool_sgtz, tool_xy, tool_xd, tool_id, tool_urine, tool_wdj, tool_uricacid
from base.management.commands import tool_it
from base.tool_health_data import get_record
from requests.packages.urllib3.util import Retry

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4146.4 Safari/537.36'}


def get_session():
    pass


def rget(*a, **k):
    s = requests.Session()
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=5, method_whitelist=frozenset(['GET', 'POST']))))
    s.mount('http://', HTTPAdapter(max_retries=Retry(total=5, method_whitelist=frozenset(['GET', 'POST']))))
    k['timeout'] = 10
    return s.get(*a, **k)


def rpost(*a, **k):
    s = requests.Session()
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=5, method_whitelist=frozenset(['GET', 'POST']))))
    s.mount('http://', HTTPAdapter(max_retries=Retry(total=5, method_whitelist=frozenset(['GET', 'POST']))))
    k['timeout'] = 10
    return s.post(*a, **k)


IP = '192.168.0.187'
url_scan = 'http://{}/gap/nodes?filter_rssi=-65&chip=0&active=1&event=1'.format(IP)
url_connect = 'http://{ip}/gap/nodes/{mac}/connection/?chip=0'
# url_connected = 'http://{ip}/gap/nodes?&connection_state=connected'.format(ip=IP)
url_sse_connect = 'http://{ip}/management/nodes/connection-state'.format(ip=IP)
url_sse_data = 'http://{ip}/gatt/nodes?event=1'.format(ip=IP)


def requests_get(*a, **k):
    try:
        return requests.get(*a, **k)
    except Exception as e:
        print(e)


def requests_post(*a, **k):
    try:
        return requests.post(*a, **k)
    except Exception as e:
        print(e)


# def _post_to_socket(data):
#     pass
# <<<<<<< HEAD
# def _post_to_socket(data):
#     tool_it.post(sys='sys', name='log', sub='sub', data=data)
# =======
def _post_to_socket(mac, data):
    #     if data.get('type') in ('血氧波形包',):
    #         return
    #   data = {'connected':1} || completed data
    url = 'http://health-t.med-value.com/users/postlog'
    log_data = {'mac': mac, 'log': data}

    #    print(log_data)
    print('_post_to_socket function...')
    data = get_record(log_data)
    #    print(data)
    if data:
        #        if data.get('address'): print(data)
        print('upload data:', data)
        return rpost(url=url, json=data, headers={'Content-Type': 'application/json;charset=UTF-8'})


#     r  = tool_it.post(sys='sys', name='log', sub='sub', data=log_data)
#     print(r)
# >>>>>>> 0b9825e2555f4b548ee820ebbc1a9fb55eacef0e
#     return
#     HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}
#     url = 'http://42.193.55.227/im/base/post_data/'
#     data = {
#     "type": "handle_post",
#     "group_name": "chat_111",
#     "data":data,
#     }
#     requests_post(url, json=data, headers=HEADERS)


devices = {
    'C0:30:00:23:58:EB': {
        'name': 'blood pressure',
        'type': 0,
        'connected': 0,
        'url_notify': 'http://{ip}/gatt/nodes/{mac}/handle/36/value/0200?',
    },
    'C2:18:08:06:31:91': {
        'name': 'glucose',
        'type': 1,
        'connected': 0,
        'url_notify': 'http://{ip}/gatt/nodes/{mac}/handle/19/value/0100?',
    },
    '84:CC:A8:D5:FC:9E': {
        'name': 'height_weight_bmi',
        'type': 2,
        'connected': 0,
        'url_notify': 'http://{ip}/gatt/nodes/{mac}/handle/45/value/0100?',
        'url_conn_ack': 'http://{ip}/gatt/nodes/{mac}/handle/42/value/130950040000000070?noresponse=1',
    },
    'C8:A3:EA:02:FE:1D': {
        'name': 'blood oxgen',
        'type': 3,
        'connected': 0,
        'url_notify': 'http://{ip}/gatt/nodes/{mac}/handle/16/value/0100?',
        'connection_type': 'random',
        'headers': {'Content-Type': 'application/json'},
    },
    'C0:17:12:01:01:C4': {
        'name': 'heart beat',
        'type': 4,
        'connected': 0,
        'connection_type': 'random',
        'url_notify': "http://{ip}/gatt/nodes/{mac}/handle/4/value/0100?"
    },
    '00:0E:0B:00:00:97': {
        'name': 'id card',
        'type': 5,
        'connected': 0,
        'connection_type': 'random',
        'url_notify': "http://{ip}/gatt/nodes/{mac}/handle/14/value/0100?",
        'headers': {'Content-Type': 'application/json'},
        #        'url_timer':'http://{ip}/gatt/nodes/{mac}/handle/11/value/AAAAAA96690003300132?noresponse=1',
        'url_timer': 'http://{ip}/gatt/nodes/{mac}/handle/11/value/AAAAAA96690003A003A0?noresponse=1',
    },
    '00:15:8B:33:25:A3': {
        'name': 'urine',
        'type': 6,
        'connected': 0,
        'url_notify': 'http://{ip}/gatt/nodes/{mac}/handle/37/value/938E050008ED00FA?',
    },
    'DF:38:8C:B8:9B:67': {
        'name': 'thermometer',
        'type': 7,
        'connected': 0,
        'connection_type': 'random',
        'url_notify': 'http://{ip}/gatt/nodes/{mac}/handle/12/value/0100?',
    },
    'F4:04:4C:10:C9:44': {
        'name': 'uric acid',
        'type': 8,
        'connected': 0,
        'connection_type': 'public',
        'url_notify': 'http://{ip}/gatt/nodes/{mac}/handle/42/value/0100?',
    }

}


def sse(url):
    client = sseclient.SSEClient(requests.get(url, stream=True))
    for event in client.events():
        yield json.loads(event.data)


def scan(devices, lock):
    macs = devices.keys()
    for d in sse(url_scan):
        mac = d.get('bdaddrs', [{}])[0].get('bdaddr')
        if mac in macs:
            if devices[mac]['connected'] == 0:
                lock.acquire()
                connect(devices, mac)
                lock.release()


# {'dataType': 'indication',
# 'handle': 35,
# 'id': 'C0:30:00:23:58:EB',
# 'value': '1E80004B005C00E507040F0B15004B00000000'}

def notify_data(devices, lock):
    for d in sse(url_sse_data):
        #        pprint.pprint(d)
        mac = d.get('id')
        value = d.get('value')
        device_type = devices[mac]['type']
        if device_type == 0:
            data = tool_yy.parse_pressure(value)

        elif device_type == 1 and len(value) >= 26:
            data = tool_yy.parse_glucose(value)

        elif device_type == 2:
            data = tool_sgtz.parse_result(value)

        elif device_type == 3:
            data = tool_xy.parse_result(value)

        elif device_type == 4:
            data = tool_xd.parse_result(value)
            if data and data.get('type') == 'time':
                requests.get(tool_xd.time_ack_url(IP, mac))

        elif device_type == 5:
            data = tool_id.parse_result(value)

        elif device_type == 6:
            print('start to test urine...')
            data = tool_urine.parse_result(value)

        elif device_type == 7:
            print('start to test thermometer')
            data = tool_wdj.parse_result(value)

        elif device_type == 8:
            print('start to test uric acid')
            data = tool_uricacid.parse_result(value)

        else:
            data = None
        if data:
            #            data['_mac_addr'] = mac
            print('notify_data function...')
            pprint.pprint(data)
            _post_to_socket(mac, data)
        else:
            print('wrong data: {}'.format(data))


def notify_connection(devices, lock):
    for d in sse(url_sse_connect):
        pprint.pprint(d)
        mac = d.get('handle')
        lock.acquire()
        if d.get('connectionState') == 'connected':
            print('connected...')
            devices[mac]['connected'] = -1 if devices.get(mac) else None
            _post_to_socket(mac, {'connected': 1})
            time.sleep(1)
            on_connected(devices, mac)
        elif d.get('connectionState') == 'disconnected':
            print('disconnected...')
            devices[mac]['connected'] = 0 if devices.get(mac) else None
            _post_to_socket(mac, {'disconnected': 1})
        else:
            raise ValueError(str(d))

        lock.release()


def on_timer(devices, mac):
    while devices[mac]['connected'] != 0:
        if not tool_id.cache:
            requests_get(devices[mac].get('url_timer').format(ip=IP, mac=mac))
        time.sleep(1)


def on_connected(devices, mac):
    print('on_connected...')
    requests.get(devices[mac]['url_notify'].format(ip=IP, mac=mac))
    if devices[mac].get('url_conn_ack'):
        requests.get(devices[mac]['url_conn_ack'].format(ip=IP, mac=mac))

    if devices[mac].get('url_timer'):
        threading.Thread(target=on_timer, args=(devices, mac)).start()


def connect(devices, mac):
    print('connecting ...', mac)
    try:
        device = devices[mac]
        devices[mac]['connected'] = -1

        data = {"type": device.get("connection_type", "public"), "discovergatt": 1, "timeout": 1500}
        url = url_connect.format(ip=IP, mac=mac)
        if not device.get('headers'):
            # launch a connection, url is the address
            r = requests.post(url, data=data)
        else:
            r = requests.post(url, data=json.dumps(data), headers=device.get('headers'))
        if r.status_code != 200:
            print('failed to connect:', r)
            devices[mac]['connected'] = 0
    except Exception as e:
        print(e)
        devices[mac]['connected'] = 0


def main():
    #    connect(devices, 'C8:A3:EA:02:FE:1D')
    #    return
    lock = threading.Lock()
    threading.Thread(target=notify_data, args=(devices, lock)).start()
    threading.Thread(target=scan, args=(devices, lock)).start()
    th = threading.Thread(target=notify_connection, args=(devices, lock))
    th.start()
    th.join()


# def debug():
#    devices = {
#        'C0:30:00:23:58:EB':{
#            'name':'blood pressure',
#            'connected':0,
#            },
#        'C2:18:08:06:31:91': {
#            'name':'glucose',
#            'connected':0,
#            }
#        }
#
#    lock = threading.Lock()
#    threading.Thread(target=notify_data,args=(devices,lock)).start()
#    threading.Thread(target=scan,args=(devices,lock)).start()
#    th = threading.Thread(target=notify_connection,args=(devices,lock))
#    th.start()
##    th.join()
#    for d in sse(url_sse_notify):
#        pprint.pprint(d)


if __name__ == "__main__":
    main()


