# coding:utf-8

name = input('enter your name.:')
age = input('enter your age:')
print('your name is %s, and your age is %s' % (name, age))
print(type(name))
print(type(age))

username = 'variable'
is_used = 'is used'
user_age = 23
user_height = 170.1

if __name__ == '__main__':
    print(username, end=' ')
    print(is_used)
    print(id(is_used))
    print(user_age)
    print(type(user_age))  # type是内置函数，判断变量类型
    print(id(user_age))  # id是内置函数，判断变量存放的内存地址
    print(type(id(user_age)))
    print('身高是:', user_height)
    print(type(user_height))
    print('年龄是%d' % user_age + '，' + '身高是%s' % user_height)
    print('年龄是%d，身高是%s...' % (user_age, user_height))
    print('测试字符串中，添加字符串\'\"，测试中')
    print('"双引号"和"单' + '引号' + '"的混搭使用...')
