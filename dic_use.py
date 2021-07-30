# coding:utf-8

store = {
    'pc': {'name': 'mac', 'price': 6666}
}

print('store: {}'.format(store.keys()))
store['phone'] = {
    'name': 'iphoneX',
    'price': 7777
}
print(store)

result = store.setdefault('headphone', {'name': 'airpods pro', 'price': 2222})
print(store)
print(result)

store.update({
    'headphone':  {'name': 'airpods pro', 'price': 1111}
})
print(store)
store.update({
    'watch': {'name': 'iwatch', 'price': 2222}
})
print(store)

test_one = {
    'name': 'hank'
}
test_two = test_one
test_two['name'] = 'lucy'
print(test_one, '123')
print(test_two)

str = None
if str:
    print('ok')
else:
    print('not ok...')
