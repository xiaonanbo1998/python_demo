# coding:utf-8

test = 'print test...'
name_cap = 'hank'
gender_case = 'MALE'
gender_lower = 'FEMALE'
hobby_upper = 'music'
major_swapcase = 'Computer Science'
salary_zfill = '10'
hobby_count = 'hank likes swimming, especially in the summer...'
tips_startswith_endswith = 'this is a tip, please be careful...'
friend_find_index = 'hank, lucy, anna'
enemy_strip = '   little child, wild animals...'
song_replace = ('Every night in my dreams'
                ' I see you,I feel you'
                ' That is how I know you go on'
                ' Far across the distance'
                ' And spaces between us'
                ' You have come to show you go on')

if __name__ == '__main__':
    print(test)
    print('fn.capitalize,', name_cap.capitalize())
    print('fn.casefold,', gender_case.casefold())
    print('fn.lower,', gender_lower.lower())
    print('fn.upper,', hobby_upper.upper())
    print('fn.swapcase,', major_swapcase.swapcase())
    print('fn.zfill,', salary_zfill.zfill(10))
    print('fn.count,', hobby_count.count('m'))
    print('fn.count,', hobby_count.count(''), len(hobby_count))
    print('fn.startswith,', tips_startswith_endswith.startswith('this'))
    print('fn.endswith,', tips_startswith_endswith.endswith('careful...'))
    print('fn.find,', friend_find_index.find('lucy'))
    print('fn.index,', friend_find_index.index('anna'))
    print('fn.strip,', enemy_strip.strip())
    print('fn.strip,', enemy_strip.strip(' '))
    print('fn.strip,', enemy_strip.strip('.'))
    print('fn.lstrip,', enemy_strip.lstrip(' '))
    print('fn.rstrip,', enemy_strip.rstrip('.'))
    print('fn.replace,', song_replace.replace('I', '我').replace('you', '你'))
