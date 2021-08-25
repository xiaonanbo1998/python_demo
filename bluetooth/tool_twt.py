"""
Created to decode the data of lasting thermometer
"""


def parse_result(value):
    # print('origin data: {}'.format(value))
    if len(value) != 20:
        return 'data error...'
    hex_data = value[14: 18]
    # print('hex_data:{}'.format(hex_data), type(hex_data))
    deci_data = int(hex_data, 16)
    # print('deci_data:{}'.format(deci_data), type(deci_data))
    return {
        'data': deci_data/100,
    }


# if __name__ == '__main__':
#     origin_data = 'F107D0000000350A888F'
    # origin_data = '3d'
    # result_data = parse_result(origin_data)
    # print('final_result:{}'.format(result_data))
