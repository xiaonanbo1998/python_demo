import numpy

result_def = {
   "00": "脉搏节律未见异常",
   "01": "疑似脉率稍快",
   "02": "疑似脉率过快",
   "03": "疑似阵发性脉率过快",
   "04": "疑似脉率稍缓",
   "05": "疑似脉率过缓",
   "06": "疑似偶发脉搏间期缩短",
   "07": "疑似脉搏间期不规则",
   "08": "疑似脉率稍快伴有偶发脉搏间期缩短",
   "09": "疑似脉率稍缓伴有偶发脉搏间期缩短",
   "0a": "疑似脉率稍缓伴有脉搏间期不规则",
   "ff": "信号质量差请重新测量"
}

cache = {}

def get_start(k, h):
    return h.index(k) + len(k)

def parse_wave(h):
    '''
    >>> parse_wave('3C') == '00111100'
    True
    '''
    return '{:08b}'.format(int(h,16))

def split_wave(h):
    l = list(parse_wave(h))
    l.reverse()
    b = int(l[0])
    l[0] = '0'
    return b, int(''.join(l), 2) // 8
    
    

def split(h):
    return [h[i:i+2] for i in range(0, len(h), 2)]

def get_wave(k, h):
    s = get_start(k,h)
    l = split(h[s:s+10])
    return [split_wave(x) for x in l]

#{'data': {'脉率数据': 85, '血氧数据': 98, '血流灌注指数': 114}, 'type': '血氧参数包'}

def get_paras(k, h):
    s = get_start(k,h)
    l = split(h[s:s+12])
    d = {
        '血氧数据':int(l[0], 16),
        '脉率数据':int(l[2]+l[1], 16),
        '血流灌注指数':int(l[3],16) if len(l) >=4 else numpy.nan, 
        }
    cache['血氧数据'] = d.get('血氧数据')
    cache['脉率数据'] = d.get('脉率数据')
    cache['血流灌注指数'] = d.get('血流灌注指数')
    return d

def get_work_status(k,h):
    s = get_start(k,h)
    l = split(h[s:s+10])
    d = {
        'mode':{'01':'点测', '02':'连续', '03':'菜单'}.get(l[0]),
        'step':{'00':'Idle', '01':'准备阶段', '02':'正在测量', '03':'播报血氧', '04':'脉率分析', '05':'点测完成'}.get(l[1]),
        }
    
    if l[1] == '02':
        d['剩余时间'] = int(l[2], 16)
    elif l[1] == '03':
        d['血氧值'] = int(l[2], 16)
        d['脉率值'] = int(l[3], 16)
    elif l[1] == '04':
        d['脉率分析结果'] = result_def.get(l[2])
        d['血氧数据'] = cache.get('血氧数据')
        d['脉率数据'] = cache.get('脉率数据')
        d['血流灌注指数'] = cache.get('血流灌注指数')
    elif l[1] == '05':
        pass
    return d
    

dt = {
    'AA550F0702':('血氧波形包',get_wave),
    'AA550F0801':('血氧参数包',get_paras),
    'AA550F0621':('工作状态数据包',get_work_status),
    }

#def is_data(h):
#    return h.startswith('AA55')
#
#def get_type(h):
#    if is_data(h):
#        return {
#            'AA550F0702':'血氧波形包',
#            'AA550F0801':'血氧参数包',
#            'AA550F0621':'工作状态数据包',
#            }.get(h[8:10])

def get_data_type(h):
    for k,v in dt.items():
        if k in h:
            return v[0], v[1](k,h)

def parse_result(h):
    for k,v in dt.items():
        if k in h:
            try:
                return {'type':v[0], 'data':v[1](k,h)}
            except Exception as e:
                print(e)

def debug():
    import pandas
    l = pandas.read_csv('notify1.csv').VALUE.to_list()
    for i,x in enumerate(l):
        print(i, x, parse_result(x))
#
#raw = '''
#0x 0 脉搏节律未见异常 No irregularity found
#0x 1 疑似脉率稍快 Suspected a little fast pulse
#0x 2 疑似脉率过快 Suspected fast pulse
#0x 3 疑似阵发性脉率过快 Suspected short run of fast pulse
#0x 4 疑似脉率稍缓 Suspected a little slow pulse
#0x 5 疑似脉率过缓 Suspected slow pulse
#0x 6 疑似偶发脉搏间期缩短 Suspected occasional short pulseinterval
#0x 7 疑似脉搏间期不规则 Suspected irregular pulse interval
#0x 8 疑似脉率稍快伴有偶发脉搏间期缩短 Suspected fast pulse with short pulseinterval
#0x 9 疑似脉率稍缓伴有偶发脉搏间期缩短 Suspected slow pulse with short pulseinterval
#0x 0a 疑似脉率稍缓伴有脉搏间期不规则 Suspected slow pulse with irregularpulse interval
#0x ff 信号质量差请重新测量 
#'''

if __name__ == '__main__':
#    import doctest
#    print(doctest.testmod(verbose=False, report=False))
    debug()
    
#    l = [x.strip().split(' ') for x in raw.splitlines() if x.strip() ]
#    l = {'{:02x}'.format(int(t[1], 16)):t[2] for t in l}
#    import json
#    print(json.dumps(l, indent=3, ensure_ascii=False))
#    print(l)
#    l = [{t[1]:t[2]} for t in l]
#    print(l)
        