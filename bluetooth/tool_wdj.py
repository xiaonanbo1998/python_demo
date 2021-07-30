"""
Created to decode the data of thermometer
"""


def parse_result(value):
    # value = '41352C34302C546F3D333634322C54613D323830'
    return_data = cut_data(value)
    final_result = {
        'data': return_data
    }
    return final_result


# extract data, length is 8, and transfer to chr
def cut_data(value):
    index = calc_index(value)
    if index is None:
        return
    part_data = value[index: index + 6]
    one = chr(int(part_data[: 2], 16))
    two = chr(int(part_data[2: 4], 16))
    third = chr(int(part_data[4: 6], 16))
    ascii_data = one + two + third
    return data_cal(ascii_data)


# to calculate the index of start
def calc_index(value):
    for i in range(20):
        if value[i] == '3' and value[i+1] == 'D':
            return int(i + 2)
        else:
            i += 1
    return None


# calculate data and get final result
def data_cal(value):
    if value[0] == '0':
        return None
    int_data = int(value)
    final_result = int_data / 10
    print('final result: {}'.format(final_result))
    return final_result


# if __name__ == '__main__':
#     origin_data = parse_result('41352C332C546F3D333536302C54613D32383237')
#     print('final data: {}'.format(origin_data))
    # index = calc_index('41352C34302C546F3D333634322C54613D323830')
    # print('index: {}'.format(index))
    # print(parse_result('41352C34302C546F3D333634322C54613D323830'))

