"""
Created to decode the data of Urine Analyzer
"""
import copy
import re
import pprint


def parse_result(value):
    # response data: 93 8E 12 00 08 04 || 00 0D 07 FF 8B 91 02 31 00 00 C0 06 00 00 || 46
    print('origin_value: {}'.format(value))
    if len(value) < 40:
        return
    # value = '938E12000804000D07FF8B9102310000C006000046'
    result_data = cut_data(value)
    return result_data


# extract part of data, four in one group
def cut_data(value):
    part_data = value[12: 40]
    part_data = re.findall(r'\w{4}', part_data)
    print('cut_data:', part_data)
    return hex_transfer_bin(part_data)


# data(16) transfer to data(2),  extend the length to 16, and create a dict
def hex_transfer_bin(value):
    data_1st = bin(int(value[0], 16))[2:].zfill(16)
    data_2nd = bin(int(value[1], 16))[2:].zfill(16)
    data_3rd = bin(int(value[2], 16))[2:].zfill(16)
    data_4th = bin(int(value[3], 16))[2:].zfill(16)
    data_5th = bin(int(value[4], 16))[2:].zfill(16)
    data_6th = bin(int(value[5], 16))[2:].zfill(16)
    data_7th = bin(int(value[6], 16))[2:].zfill(16)

    binary_data = dict()
    binary_data['SN'] = data_1st[6:]
    binary_data['effective'] = data_2nd[2:]
    binary_data['TmDay'] = data_3rd[:5]
    binary_data['TmMon'] = data_3rd[5: 9]
    binary_data['TmYear'] = data_3rd[9:]
    binary_data['LEU'] = data_4th[2: 5]    # 白细胞
    binary_data['TmMinute'] = data_4th[5: 11]
    binary_data['TmHour'] = data_4th[11:]
    binary_data['BLD'] = data_5th[1: 4]    # 潜血
    binary_data['PH'] = data_5th[4: 7]    # pH值
    binary_data['PRO'] = data_5th[7: 10]    # 蛋白质
    binary_data['UBG'] = data_5th[10: 13]    # 尿胆原
    binary_data['NIT'] = data_5th[13:]    # 亚硝酸盐
    binary_data['PL'] = data_6th[: 1]
    binary_data['VC'] = data_6th[1: 4]    # 维生素C
    binary_data['GLU'] = data_6th[4: 7]    # 葡萄糖
    binary_data['BIL'] = data_6th[7: 10]   # 胆红素
    binary_data['KET'] = data_6th[10: 13]  # 酮体
    binary_data['SG'] = data_6th[13:]  # 比重
    binary_data['CRE'] = data_7th[7: 10]   # 肌酐
    binary_data['CA'] = data_7th[10: 13]   # 钙离子
    binary_data['MA'] = data_7th[13:]  # 微量白蛋白
    print(binary_data)
    # pprint.pprint(binary_data)
    return bin_transfer_deci(binary_data)


# data(2) transfer to data(10)
def bin_transfer_deci(value):
    decimal_data = copy.deepcopy(value)
    for key in decimal_data:
        temp = int(decimal_data[key], 2)
        decimal_data[key] = temp
    # print('decimal_data: {}'.format(decimal_data))
    pprint.pprint(decimal_data)
    return deci_transfer_result(decimal_data)


# data(10) transfer to final result
def deci_transfer_result(value):
    real_result = dict()
    # real_result['LEU'] = decode_leu(value)
    real_result['白细胞'] = decode_leu(value)
    # real_result['NIT'] = decode_nit(value)
    real_result['亚硝酸盐'] = decode_nit(value)
    # real_result['UBG'] = decode_ubg(value)
    real_result['尿胆原'] = decode_ubg(value)
    # real_result['PRO'] = decode_pro(value)
    real_result['蛋白质'] = decode_pro(value)
    # real_result['PH'] = decode_ph(value)
    real_result['pH值'] = decode_ph(value)
    # real_result['BLD'] = decode_bld(value)
    real_result['潜血'] = decode_bld(value)
    # real_result['SG'] = decode_sg(value)
    real_result['比重'] = decode_sg(value)
    # real_result['KET'] = decode_ket(value)
    real_result['胴体'] = decode_ket(value)
    # real_result['BIL'] = decode_bil(value)
    real_result['胆红素'] = decode_bil(value)
    # real_result['GLU'] = decode_glu(value)
    real_result['葡萄糖'] = decode_glu(value)
    # real_result['VC'] = decode_vc(value)
    real_result['维生素C'] = decode_vc(value)
    # real_result['MA'] = decode_ma(value)
    real_result['微量白蛋白'] = decode_ma(value)
    # real_result['CRE'] = decode_cre(value)
    real_result['肌酐'] = decode_cre(value)
    # real_result['CA'] = decode_ca(value)
    real_result['钙离子'] = decode_ca(value)

    pprint.pprint(real_result)
    # pprint.pprint(calc_score(real_result))
    print(calc_score(real_result)['score'])
    return real_result


def decode_leu(value):
    leu = ''
    data = ''
    if value['LEU'] == 0:
        leu = '-'
        data = '阴性'
    elif value['LEU'] == 1:
        leu = '+-'
        data = '15'
    elif value['LEU'] == 2:
        leu = '+1'
        data = '70'
    elif value['LEU'] == 3:
        leu = '+2'
        data = '125'
    elif value['LEU'] == 4:
        leu = '+3'
        data = '500'
    else:
        leu = '/'
        data = '/'

    data = data if data == '阴性' or data == '/' else data + ' Cells/μl'
    return data


def decode_nit(value):
    nit = ''
    data = ''
    if value['NIT'] == 0:
        nit = '-'
        data = '阴性'
    elif value['NIT'] == 1:
        nit = '+'
        data = '阳性'
    else:
        nit = '/'
        data = '/'

    return data


def decode_ubg(value):
    ubg = ''
    data = ''
    if value['UBG'] == 0:
        ubg = '-'
        data = '3.2/16'
    elif value['UBG'] == 1:
        ubg = '+1'
        data = '32'
    elif value['UBG'] == 2:
        ubg = '+2'
        data = '64'
    elif value['UBG'] == 3:
        ubg = '+3'
        data = '128'
    else:
        ubg = '/'
        data = '/'

    data = data if data == '/' else data + ' μmol/l'
    return data


def decode_pro(value):
    pro = ''
    data = ''
    if value['PRO'] == 0:
        pro = '-'
        data = '阴性'
    elif value['PRO'] == 1:
        pro = '+-'
        data = '微量'
    elif value['PRO'] == 2:
        pro = '+1'
        data = '0.3'
    elif value['PRO'] == 3:
        pro = '+2'
        data = '1.0'
    elif value['PRO'] == 4:
        pro = '+3'
        data = '3.0'
    elif value['PRO'] == 5:
        pro = '+4'
        data = '>20.0'
    else:
        pro = '/'
        data = '/'

    data = data if data == '阴性' or data == '微量' or data == '/' else data + ' g/l'
    return data


def decode_ph(value):
    ph = ''
    if value['PH'] == 0:
        ph = '5.0'
    elif value['PH'] == 1:
        ph = '6.0'
    elif value['PH'] == 2:
        ph = '6.5'
    elif value['PH'] == 3:
        ph = '7.0'
    elif value['PH'] == 4:
        ph = '7.5'
    elif value['PH'] == 5:
        ph = '8.0'
    elif value['PH'] == 6:
        ph = '8.5'
    else:
        ph = '/'

    return ph


def decode_bld(value):
    bld = ''
    data = ''
    if value['BLD'] == 0:
        bld = '-'
        data = '阴性'
    elif value['BLD'] == 1:
        data = '微量'
        bld = '+-'
    elif value['BLD'] == 2:
        bld = '+1'
        data = '25'
    elif value['BLD'] == 3:
        bld = '+2'
        data = '80'
    elif value['BLD'] == 4:
        bld = '+3'
        data = '200'
    else:
        bld = '/'
        data = '/'

    data = data if data == '阴性' or data == '微量' or data == '/' else data + ' Cells/μl'
    return data


def decode_sg(value):
    sg = ''
    if value['SG'] == 0:
        sg = '1.000'
    elif value['SG'] == 1:
        sg = '1.005'
    elif value['SG'] == 2:
        sg = '1.010'
    elif value['SG'] == 3:
        sg = '1.015'
    elif value['SG'] == 4:
        sg = '1.020'
    elif value['SG'] == 5:
        sg = '1.025'
    elif value['SG'] == 6:
        sg = '1.030'
    else:
        sg = '/'

    return sg


def decode_ket(value):
    ket = ''
    data = ''
    if value['KET'] == 0:
        ket = '-'
        data = '阴性'
    elif value['KET'] == 1:
        ket = '+-'
        data = '0.5'
    elif value['KET'] == 2:
        ket = '+1'
        data = '1.5'
    elif value['KET'] == 3:
        ket = '+2'
        data = '4.0'
    elif value['KET'] == 4:
        ket = '+3'
        data = '8.0'
    elif value['KET'] == 5:
        ket = '+4'
        data = '16.0'
    else:
        ket = '/'
        data = '/'

    data = data if data == '阴性' or data == '/' else data + ' mmol/l'
    return data


def decode_bil(value):
    bil = ''
    data = ''
    if value['BIL'] == 0:
        bil = '-'
        data = '阴性'
    elif value['BIL'] == 1:
        bil = '+1'
        data = '17'
    elif value['BIL'] == 2:
        bil = '+2'
        data = '50'
    elif value['BIL'] == 3:
        bil = '+3'
        data = '100'
    else:
        bil = '/'
        data = '/'

    data = data if data == '阴性' or data == '/' else data + ' μmol/l'
    return data


def decode_glu(value):
    glu = ''
    data = ''
    if value['GLU'] == 0:
        glu = '-'
        data = '阴性'
    elif value['GLU'] == 1:
        glu = '+-'
        data = '5'
    elif value['GLU'] == 2:
        glu = '+1'
        data = '15'
    elif value['GLU'] == 3:
        glu = '+2'
        data = '30'
    elif value['GLU'] == 4:
        glu = '+3'
        data = '60'
    elif value['GLU'] == 5:
        glu = '+4'
        data = '110'
    else:
        glu = '/'
        data = '/'

    data = data if data == '阴性' or data == '/' else data + ' mmol/l'
    return data


def decode_vc(value):
    vc = ''
    data = ''
    if value['VC'] == 0:
        vc = '-'
        data = '阴性'
    elif value['VC'] == 1:
        vc = '+-'
        data = '0.6'
    elif value['VC'] == 2:
        vc = '+1'
        data = '1.4'
    elif value['VC'] == 3:
        vc = '+2'
        data = '2.8'
    elif value['VC'] == 4:
        vc = '+3'
        data = '5.6'
    else:
        vc = '/'
        data = '/'

    data = data if data == '阴性' or data == '/' else data + ' mmol/l'
    return data


def decode_ma(value):
    ma = ''
    if value['MA'] == 0:
        ma = '0'
    elif value['MA'] == 1:
        ma = '30'
    elif value['MA'] == 2:
        ma = '80'
    elif value['MA'] == 3:
        ma = '150'
    else:
        ma = '/'

    ma = ma if ma == '/' else ma + ' mg/l'
    return ma


def decode_cre(value):
    cre = ''
    if value['CRE'] == 0:
        cre = '0.9'
    elif value['CRE'] == 1:
        cre = '4.4'
    elif value['CRE'] == 2:
        cre = '17.7'
    elif value['CRE'] == 3:
        cre = '26.5'
    else:
        cre = '/'

    cre = cre if cre == '/' else cre + ' mmol/l'
    return cre


def decode_ca(value):
    ca = ''
    if value['CA'] == 0:
        ca = '0'
    elif value['CA'] == 1:
        ca = '2.5'
    elif value['CA'] == 2:
        ca = '5.0'
    elif value['CA'] == 3:
        ca = '10'
    else:
        ca = '/'

    return ca + ' mmol/l'


# calculate the score
def calc_score(value):
    status = dict()
    status['白细胞'] = '正常' if value['白细胞'] == '阴性' else '异常'
    status['亚硝酸盐'] = '正常' if value['亚硝酸盐'] == '阴性' else '异常'
    status['尿胆原'] = '正常' if value['尿胆原'] == '3.2/16 μmol/l' else '异常'
    status['蛋白质'] = '正常' if value['蛋白质'] == '阴性' else '异常'
    status['pH值'] = '正常'
    status['潜血'] = '正常' if value['潜血'] == '阴性' else '异常'
    status['比重'] = '正常' if value['比重'] == '1.015' or value['比重'] == '1.020' or value['比重'] == '1.025' else '异常'
    status['胴体'] = '正常' if value['胴体'] == '阴性' else '异常'
    status['胆红素'] = '正常' if value['胆红素'] == '阴性' else '异常'
    status['葡萄糖'] = '正常' if value['葡萄糖'] == '阴性' else '异常'
    status['维生素C'] = '正常' if value['维生素C'] == '阴性' else '异常'
    status['微量白蛋白'] = '正常' if value['微量白蛋白'] == '0 mg/l' or value['微量白蛋白'] == '30 mg/l' else '异常'
    status['肌酐'] = '正常' if value['肌酐'] == '4.4 mmol/l' or value['肌酐'] == '17.7 mmol/l' else '异常'
    status['钙离子'] = '正常'

    status['score'] = 100
    for i in status:
        status['score'] = status['score'] if status[i] == '正常' else status['score'] - 7
    status['score'] += 7

    return status


# get the vallist
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


if __name__ == '__main__':
    # parse_result('938E1200080400243FFF088710080641809500DB')
    parse_result('938E1200080400253FFFD39514AB020182560080')

