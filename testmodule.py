def test_func(message):
    print('test_func' + str(message))
    with open('testmodule.txt', 'w') as f:
        f.write('Test Module performed')


def test_func_1(message):
    print('test_func_1 ' + message)
