# coding:utf-8

print('print test...')
name_one = ['hank', 'anna']
name_two = name_one + name_one
name_three = name_one * 3
# name_four = list()
name_four = list()
name_four.append('lucy')
name_four.append(None)
name_five = []
name_five.insert(0, 'anna')
name_five.insert(1, None)
animal = ['dog', 'dog', 'cat']
animal_num = animal.count('dog')

data = {
    '123': {
        'name': 'hank'
    },
    '456': {
        'name': 'lucy',
        'gender': 'female'
    }
}
print('data_one:', data.keys())
print('data_two:', data.items())
print('data_three:', data.get('123'))
print('--------------------------------')
for k in data.items():
    # print('for:', k)
    pass

if __name__ == '__main__':
    print(name_one)
    print(name_two)
    print(name_three)
    print(name_four)
    print(name_five)
    print(animal_num)
