# coding:utf-8

str_one = ['a', 'b', 'c']
print('before, id of str:', id(str_one))
str_one = str_one + ['d', 'e', 'f']
print('after, id of str:', id(str_one))

list_one = [1, 2, 3]
print('before, id:', id(list_one))
list_one = list_one + [4, 5, 6]
print('after, id:', id(list_one))

tuple_one = (11, 12, 13)
print('before, id of tuple:', id(tuple_one))
tuple_one = tuple_one + (14, 15, 16)
print('after, id of tuple:', id(tuple_one))

dict_one = {'name': 'hank', 'age': 12, 'gender': 'male'}
print('before, id of dict', id(dict_one))
# dict_one = dict_one + {'height': 170}
# print('after, id of dict:', id(dict_one))


if __name__ == '__main__':
    print('---------------------------------------')
    print('str_one:', str_one)
    print('str_one * 2 = ', str_one * 2)
    print('list_one:', list_one)
    print('list_one * 2 = ', list_one * 2)
    print('tuple_one:', tuple_one)
    print('tuple_one * 2 = ', tuple_one * 2)
    print('dict_one:', dict_one)
