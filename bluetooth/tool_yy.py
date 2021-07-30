'''
Created on 2021年4月17日

@author: winston
'''
import re
import datetime

def remove_space(s):
    return re.sub('\s+','', s)

def pick(s, start=0, length=None, pick_all=False, low_high=True):
    """
    >>> pick(sample, 0, 2) == '1e'
    True
    >>> pick(sample, 0, 4) == '5f1e'
    True
    >>> pick(sample, 0, 4, low_high=False) == '1e5f'
    True
    >>> pick(sample, -4, 4) == '0004'
    True
    >>> pick('31003900380037003100310031003900', 0, 4) == '0031'
    True
    >>> pick('31003900380037003100310031003900', length=4, pick_all=True)
    ['0031', '0039', '0038', '0037', '0031', '0031', '0031', '0039']
    """
    def _pick(s, start, length):
        if length == 4 and low_high:
            start = start if start >=0 else len(s) + start
            l = [s[start+i*2:start+i*2+2] for i in range(length // 2)]
            l.reverse()
            return ''.join(l)
        return s[start:start+length]
    if not pick_all:
        return _pick(s, start, length)

    return [_pick(s, start+i*length, length) for i in range(len(s) // length)]


def pick_as_int(s, start=0, length=None, d='x', pick_all=False, low_high=True):
    """
    >>> pick_as_int('0000000000000100', -4, 2, 'b') == 1
    True
    >>> pick_as_int('0000000000000100', -5, 2, 'b') == 0
    True
    >>> pick_as_int(sample, 2, 4) == 95
    True
    >>> pick_as_int(sample, 6, 4) == 65
    True
    >>> pick_as_int(sample, 10, 4) == 75
    True
    >>> pick_as_int(sample, 14, 4) == 2017
    True
    >>> pick_as_int(sample, 18, 2) == 7
    True
    >>> pick_as_int(sample, 20, 2) == 12
    True
    >>> pick_as_int(sample, 22, 2) == 8
    True
    >>> pick_as_int(sample, 24, 2) == 10
    True
    >>> pick_as_int(sample, 26, 2) == 25
    True
    >>> pick_as_int(sample, 28, 4) == 64
    True
    >>> pick_as_int(sample, 32, 2) == 0
    True
    >>> pick_as_int('31003900380037003100310031003900',length=4, pick_all=True)
    [49, 57, 56, 55, 49, 49, 49, 57]
    """
    l = pick(s, start, length, pick_all=pick_all,low_high=low_high)
    if not pick_all:
        return int(('0%s' % d) + l, 0)
    return [int(('0%s' % d) + x, 0) for x in l]

def parse_ascii(s):
    '''
    >>> parse_ascii('31003900380037003100310031003900') == '19871119'
    True
    '''
    l = pick_as_int(s, length=4, d='x', pick_all=True)
    return ''.join(map(lambda x:chr(x), l))

def parse_unicode(s):
    '''
    >>> parse_unicode('D65E664EC560200020002000200020002000200020002000200020002000') is not None
    True
    '''
    l = pick(s, start=0, length=4, pick_all=True)
    r = []
    for x in l:
        r.append(ord('\\'))
        r.append(ord('u'))
        for y in x:
            r.append(ord(y))
    return bytes(r).decode('unicode_escape').strip()

def pick_binary(s, start, length):
    """
    >>> pick_binary(sample, 0, 2) == '00011110'
    True
    >>> pick_binary(sample, -4, 4) == '0000000000000100'
    True
    """
    return ("{:0%db}" % (4*length)).format(pick_as_int(s, start, length))

def parse_pressure(s):
    s = remove_space(s)
    flag = pick_binary(s, 0, 2)
    status = pick_binary(s, -4, 4)
    return {
        '测量单位': ('mmHg','kPa')[int(flag[-1])],
        '时间标识': int(flag[-2]),
        '脉率标识': int(flag[-3]),
        '用户Id标识': int(flag[-4]),
        '测量状态标识': int(flag[-5]),
        '误动检测': int(status[-1]),
        '袖带佩戴检测':int(status[-2]),
        '心率不齐检测':int(status[-3]),
        '脉搏范围检测':('范围内', '超过最高值','低于最低值','保留')[pick_as_int(status, -5, 2, 'b')],
        '不正确体位检测':int(status[-6]),
        '收缩压':pick_as_int(s, 2, 4),
        '舒张压':pick_as_int(s, 6, 4),
        '平均动脉压':pick_as_int(s, 10, 4),
        '年':pick_as_int(s, 14, 4),
        '月':pick_as_int(s, 18, 2),
        '日':pick_as_int(s, 20, 2),
        '时':pick_as_int(s, 22, 2),
        '分':pick_as_int(s, 24, 2),
        '秒':pick_as_int(s, 26, 2),
        '脉搏':pick_as_int(s, 28, 4),
        'UserId':pick_as_int(s, 32, 2),   
        }

def parse_intermediate_cuff_pressure(s):
    '''
    >>> parse_intermediate_cuff_pressure('1e 37 00 ff 07 ff 07 e1 07 07 0c 08 0a 19 ff 07 00 10 00') == 55
    True
    '''
    return pick_as_int(remove_space(s), 2, 4)


def format_time_string(year, month, day, hour, min, sec):
    '''
    >>> format_time_string(2017, 9, 30, 12, 40, 00) == 'e107091e0c2800000000'
    True
    >>> format_time_string(2017, 9, 30, 12, 40, 16) == 'e107091e0c2810000000'
    True
    '''
    return '{year[2]}{year[3]}{year[0]}{year[1]}{month}{day}{hour}{min}{sec}000000'.format(
            year='{:04x}'.format(year),
            month='{:02x}'.format(month),
            day='{:02x}'.format(day),
            hour='{:02x}'.format(hour),
            min='{:02x}'.format(min),
            sec='{:02x}'.format(sec),
            )

def time_now():
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    return format_time_string(t.year, t.month, t.day, t.hour, t.minute, t.second)


def parse_glucose(s):
    '''
    >>> d = parse_glucose(sample_gc)
    >>> d['Time offset Present'] == 0
    True
    >>> d['Sensor status annunciation present'] == 0
    True
    >>> d['序号'] == 6
    True
    >>> d['年'] == 2019
    True
    >>> d['月'] == 4
    True
    >>> d['日'] == 26
    True
    >>> d['时'] == 10
    True
    >>> d['分'] == 39
    True
    >>> d['秒'] == 57
    True
    >>> d['血糖值'] == 12.0
    True
    >>> d['采样部位'] == '指尖静脉血'
    True
    >>> d['采样类型'] == 'Capillary Whole blood'
    True
    '''
    s = remove_space(s)
    flag = pick_binary(s, 0, 2)
    status = pick_binary(s, -4, 4)
    d = {
        'Time offset Present': int(flag[-1]),
        'Glucose concentration,type & sample location present': int(flag[-2]),
        '单位': ('kg/L','mol/L')[int(flag[-3])],
        'Sensor status annunciation present': int(flag[-4]),
        'Context information follows': int(flag[-5]),
        '序号':pick_as_int(s, 2, 4),
        '年':pick_as_int(s, 6, 4),
        '月':pick_as_int(s, 10, 2),
        '日':pick_as_int(s, 12, 2),
        '时':pick_as_int(s, 14, 2),
        '分':pick_as_int(s, 16, 2),
        '秒':pick_as_int(s, 18, 2),
        }
    i = 20 + d['Time offset Present'] * 4
    gc = pick(s, i, 4)
    c = pick_as_int(gc, 0, 1)
    g = pick_as_int(gc, 1, 3)
    v = g * (10 ** (c+3-16))
    d['血糖值'] = v
    j = i + 4
    d['采样部位'] = {1:'指尖静脉血', 2:'Alternate Site Test', 3:'耳垂', 4:'质控液', 15:'Sample Location value not available'}.get(pick_as_int(s, j, 1))
    j = i + 4 + 1
    t = {1: 'Capillary Whole blood', 2: 'Capillary Plasma', 3: 'Venous Whole blood', 4: 'Venous Plasma', 5: 'Arterial Whole blood', 6: 'Arterial Plasma', 7: 'Undetermined Whole blood', 8: 'Undetermined Plasma', 9: 'Interstitial Fluid (ISF)', 10: 'Control Solution'}
    d['采样类型'] = t.get(pick_as_int(s, j, 1))
    return d

if __name__ == '__main__':
    sample = remove_space("1e 5f 00 41 00 4b 00 e1 07 07 0c 08 0a 19 40 00 00 04 00")
    sample_gc = remove_space("06 06 00 e3 07 04 1a 0a 27 39 78 c0 11")
    import doctest
    print(doctest.testmod(verbose=False, report=False))
