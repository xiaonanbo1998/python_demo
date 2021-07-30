# coding:utf-8

str_one = 'this is the first string'
str_two = '''
    this string is used to test the punctuation, and make sure this is  a string data...
'''
str_three = """this is the third string?"""
result_one = 'second' in str_one
result_second = 'first' not in str_one
result_third = ''
list_one = ['one', ' ', '', 123]

if __name__ == '__main__':
    print('str_one_content:', str_one)
    print('str_two_content:', str_two)
    print('str_one_id:',  id(str_one))
    print('str_one_type:', type(str_one))
    print('str_two_type:', type(str_two))
    print('str_three_type:', type(str_three))
    print('str_one_len:', len(str_one))
    print('result_one:', result_one)
    print('result_second:', result_second)
    print('max:', max(str_one))
    print('min:', min(str_one))  # 空格是最小的字符
    print(len(result_third))
    print(bool(result_third))
    print('list_one:', list_one)
    print(len(list_one))
    print(len('41352C37352C546F3D'))
    print(len('41352C332C546F3D'))
