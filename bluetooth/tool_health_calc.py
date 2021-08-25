'''
Created on 2021年5月13日

@author: winston
'''
import pandas
import os
import numpy

DF = pandas.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'health_calc.csv'), encoding='cp936')
DF.sempty = DF.sempty.fillna(0)


def get_bmi(h, w):
    return w / (h ** 2)


def calc_s(s, v):
    if not s.empty:
        s = s.iloc[0]
        return (v - s.start) * (s.high - s.low) / (s.end - s.start) + s.low
    return numpy.nan


def calc_bmi_score(h, w):
    '''
    >>> int(calc_bmi_score(h=1.67, w=70) * 100) == 8725
    True
    '''
    df = DF
    bmi = get_bmi(h, w)
    df = df[df.type == 'BMI']
    s = df[(bmi > df.start) & (bmi <= df.end)].iloc[0:1]
    return calc_s(s, bmi)


def calc_hb(v):
    '''
    >>> calc_hb(v=0) == 100
    True
    >>> calc_hb(v=1) == 80
    True
    '''
    df = DF
    df = df[df.type == '心电']
    s = df[(v == df.start)].iloc[0:1]
    return s.low


def cacl_bp_ss(v):
    '''
    >>> cacl_bp_ss(v=110) == 100
    True
    >>> cacl_bp_ss(v=150) == 90
    True
    '''
    df = DF
    df = df[df.type == '收缩压']
    s = df[(v > df.start) & (v <= df.end)].iloc[0:1]
    return calc_s(s, v)


def cacl_bp_sz(v):
    '''
    >>> cacl_bp_sz(v=88) == 100
    True
    >>> cacl_bp_sz(v=95) == 90
    True
    >>> cacl_bp_sz(v=110)
    '''
    df = DF
    df = df[df.type == '舒张压']
    s = df[(v > df.start) & (v <= df.end)].iloc[0:1]
    return calc_s(s, v)


def cacl_bp_xy(v):
    '''
    >>> int(cacl_bp_xy(v=0.93) * 10) == 834
    True
    >>> cacl_bp_xy(v=0.95) == 99
    True
    '''
    df = DF
    df = df[df.type == '血氧']
    s = df[(v > df.start) & (v <= df.end)].iloc[0:1]
    return calc_s(s, v)


def cacl_bp_xt(v, is_semtpy=1):
    '''
    >>> cacl_bp_xt(v=7, is_semtpy=1) == 90
    True
    >>> cacl_bp_xt(v=7, is_semtpy=0) == 100
    True
    >>> int(cacl_bp_xt(v=3,is_semtpy= 0) * 100) == 3846
    True
    '''
    df = DF
    df = df[df.type == '血糖']
    s = df[(v > df.start) & (v <= df.end) & (df.sempty == is_semtpy)]
    if s.empty and not is_semtpy:
        s = df[(v > df.start) & (v <= df.end) & (df.sempty == 1)].iloc[0:1]
    else:
        s = s.iloc[0:1]
    return calc_s(s, v)


def cacl_bp_nj(value):
    # df = DF
    # df = df[df.type == '潜血']
    # s = df[(v > df.start) & (v <= df.end)].iloc[0:1]
    status = dict()
    status['白细胞'] = '正常' if value['白细胞'] == '阴性' else '异常'
    status['亚硝酸盐'] = '正常' if value['亚硝酸盐'] == '阴性' else '异常'
    status['尿胆原'] = '正常' if value['尿胆原'] == '3.2/16' else '异常'
    status['蛋白质'] = '正常' if value['蛋白质'] == '阴性' else '异常'
    status['pH值'] = '正常'
    status['潜血'] = '正常' if value['潜血'] == '阴性' else '异常'
    status['比重'] = '正常' if value['比重'] == '1.015' or value['比重'] == '1.020' or value['比重'] == '1.025' else '异常'
    status['胴体'] = '正常' if value['胴体'] == '阴性' else '异常'
    status['胆红素'] = '正常' if value['胆红素'] == '阴性' else '异常'
    status['葡萄糖'] = '正常' if value['葡萄糖'] == '阴性' else '异常'
    status['维生素C'] = '正常' if value['维生素C'] == '阴性' else '异常'
    status['微量白蛋白'] = '正常' if value['微量白蛋白'] == '0' or value['微量白蛋白'] == '30' else '异常'
    status['肌酐'] = '正常' if value['肌酐'] == '4.4' or value['肌酐'] == '17.7' else '异常'
    status['钙离子'] = '正常'

    status['score'] = 100
    for i in status:
        status['score'] = status['score'] if status[i] == '正常' else status['score'] - 7
    status['score'] += 7

    return status


def cacl_bp_wd(v):
    score = 100 if 36.0 < v < 37.3 else 60
    return score


def cacl_bp_uricacid(v):
    # 4100葡萄糖，5100尿酸，6100总胆固醇
    if v.get('sequence number') == '4100':
        if 1.10 <= v.get('concentration') <= 33.3:
            return 100
        else:
            return 60
    elif v.get('sequence number') == '5100':
        if 0.18 <= v.get('concentration') <= 1.19:
            return 100
        else:
            return 60
    elif v.get('sequence number') == '6100':
        if 2.59 <= v.get('concentration') <= 10.35:
            return 100
        else:
            return 60
    else:
        return 60


def cacl_bp_twt(v):
    score = 100 if 36.0 < v < 37.3 else 60
    return score


def cacl_xl(v):
    '''
    >>> int(cacl_xl(v=90) * 1) == 100
    True
    >>> cacl_xl(v=120) == 90
    True
    >>> cacl_xl(v=50) == 90
    True
    '''
    df = DF
    df = df[df.type == '心率']
    s = df[(v > df.start) & (v <= df.end)].iloc[0:1]
    return calc_s(s, v)


def get_status(v):
    return 1 if v >= 90 else 2


# BMI
def get_status_bmi(h, w):
    return get_status(calc_bmi_score(h, w))


# 心电
def get_status_hb(v):
    return get_status(calc_hb(v))


# 血氧
def get_status_xy(v):
    return get_status(cacl_bp_xy(v))


# 心率
def get_status_xl(v):
    return get_status(cacl_xl(v))


# 血糖
def get_status_xt(v):
    return get_status(cacl_bp_xt(v))


# 收缩压
def get_status_sz(v):
    return get_status(cacl_bp_sz(v))


# 舒张压
def get_status_ss(v):
    return get_status(cacl_bp_ss(v))


# 尿液
def get_status_ny(v):
    return cacl_bp_nj(v)


# 体温
def get_status_tw(v):
    return get_status(cacl_bp_wd(v))


# 葡萄糖，尿酸，总胆固醇
def get_status_uricacid(v):
    return get_status(cacl_bp_uricacid(v))


# 体温贴
def get_status_twt(v):
    return get_status(cacl_bp_twt(v))


if __name__ == '__main__':
    import doctest

    print(doctest.testmod(verbose=False, report=False))

