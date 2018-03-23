import time
import random
import os


def zipf():  # 使用户请求文件的频率满足zipf分布
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 假设文件流行的排名，（可更改）
    for i in range(len(a)):
        a[i] = 1 / a[i]
        if i != 0:
            a[i] = a[i] + a[i - 1]
    r = random.uniform(0, a[len(a) - 1])
    if r < a[0]:
        return 0
    for i in range(1, len(a)):
        if a[i - 1] < r <= a[i]:
            return i


def auto_request(client_file, all_files):
    while True:
        if random.randint(0, 9) >= 5:  # 设定用户需要文件的时间概率，可更改
            print('I will not send a requestion!')
            time.sleep(5)
        else:
            file_without = []  # 该客户端所没有的文件
            for i in range(len(all_files)):
                if client_file.count(str(all_files[i])) == 0:
                    file_without.append(all_files[i])
            if len(file_without) == 0:
                return False  # 回复False表示已拥有所有文件

            m = zipf()
            if all_files[m] in file_without:
                filename = all_files[m]
                return filename

            # m = random.randint(0, len(file_without)-1)#此处可更改
            else:
                print('I have ', all_files[m], ',I will not send a requestion!')
                continue


def get_size(file_dir):  # 获取所含有文件大小
    file_list = os.listdir(file_dir)
    size = 0
    for file in file_list:
        size = size + os.path.getsize(file_dir + '/' + file)
    return size

