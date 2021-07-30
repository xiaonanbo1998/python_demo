example_data = '024100ee070c1403220576a211'
origin_data = '064100E307051B0A100EE1C111'
data_two = '064100E307051B0D3315D1B411'   # 12.3mmol/L
data_three = '064100E307051B12382894B411'   # 11.7mmol/L


# 数据解析源头
def parse_result(value):
    return cut_data(value)


# 根据不同字段位数，拆分数据
def cut_data(value):
    # print('origin_data: ', value)
    dealt_data = {
        'unit': 'kg/L',
        'sequence number': value[2: 6],
        'year': value[6: 10],
        'month': value[10: 12],
        'day': value[12: 14],
        'hour': value[14: 16],
        'minute': value[16: 18],
        'second': value[18: 20],
        'concentration': value[20: 24],
        'type and location': value[24: 26]
    }
    # print('dealt_data: {}'.format(dealt_data))

    return hex_to_binary(dealt_data)


# 字段值，十六进制转十进制
def hex_to_binary(value):
    analyze_data = value
    # 高低位置换
    year = analyze_data['year'][2: 4] + analyze_data['year'][0: 2]
    analyze_data['year'] = int(year, 16)
    analyze_data['month'] = int(analyze_data['month'], 16)
    analyze_data['day'] = int(analyze_data['day'], 16)
    analyze_data['hour'] = int(analyze_data['hour'], 16)
    analyze_data['minute'] = int(analyze_data['minute'], 16)
    analyze_data['second'] = int(analyze_data['second'], 16)
    # 高低位置换
    concentration = analyze_data['concentration'][2:] + analyze_data['concentration'][:2]
    analyze_data['concentration'] = concentration
    first_bit = calc_complement(analyze_data['concentration'])
    left_bits = calc_concentration(analyze_data['concentration'])
    analyze_data['concentration'] = round((10 ** (-first_bit) * left_bits) * 1000, 2)
    analyze_data['type and location'] = 'Type: Capillary Whole Blood Sample & Location: Finger'
    # print('analyze_data: {}'.format(analyze_data))
    return analyze_data


# 浓度计算
def calc_concentration(value):
    # decimal_data = str(int(value[1:], 16))
    decimal_data = int(value[1:], 16)
    return decimal_data


# 补码运算
def calc_complement(value):
    binary_data = str()
    reverse_data = str()
    # 1.十六进制转二进制
    binary_data = bin(int(value[:1], 16))[2:]
    # print('binary_data: ', binary_data)
    # 2.二进制对位取反
    for i in range(4):
        reverse_data += str(int(binary_data[i]) ^ 1)
    # print('reverse_data: ', reverse_data)
    # 3.二进制转十进制，再加一
    decimal_data = int(reverse_data, 2) + 1
    # print(decimal_data)
    # return str(decimal_data)
    return decimal_data


# if __name__ == '__main__':
    # cut_data(example_data)
    # cut_data(origin_data)
    # cut_data(data_two)
