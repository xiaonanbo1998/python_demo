# coding:utf-8

a = 300
b = 300

if __name__ == '__main__':
    print('a is b:', a is b)
    print(id(a), id(b))
    b += 1
    print('a is b:', a is b, b)
    print(id(a), id(b))
    a += 1
    print('a is b:', a is b, a)
    print(id(a), id(b))
    a = 302
    print(id(a), id(b))
