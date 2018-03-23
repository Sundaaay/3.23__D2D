# a = 123.456
# print(a, type(a))
# b = str(a)
# print(b, type(b))
# c = float(b)
# print(c)
# print(type(c))

# a = 'abc'
# print(a.split('$'))

# a = ['aa','bb']
# a.remove('aa')
# print(a)

import _thread
import time

# 为线程定义一个函数
# def print_time( threadName, delay):
#    count = 0
#    while True:
#       time.sleep(delay)
#       count += 1
#       print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
#
# # 创建两个线程
# try:
#    _thread.start_new_thread( print_time, ("Thread-1", 1, ) )
# except:
#    print ("Error: 无法启动线程")
# while True:
#     print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#     time.sleep(2)
# while 1:
#    pass

a = str(123.123)
b = str(456.456)
a = float(a)
b = float(b)
c = [a, b]
print(c, type(c), type(c[0]))



