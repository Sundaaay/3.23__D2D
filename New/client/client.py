import socket
import time
import json
import os
import _thread
from .file_system import auto_request, get_size


# 建立socket连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = '127.0.0.1', 9999
s.connect((host, port))

FILE_DIR = os.getcwd()+'/client_dir'  # 文件存储路径

# 第一次静态接收，客户端名称
client_name = s.recv(4096)
print('I am', str(client_name, "utf-8"))

# 第二次静态接收，所有文件名
all_files = json.loads(str(s.recv(4096), "utf-8"))
print('All of the files are ', all_files)

# 第一次静态发送，初始化文件名
client_file = os.listdir(FILE_DIR)
s.sendall(json.dumps(client_file).encode())


def send_position(s):  # 参数中应传入一个socket.socket实例，在函数内直接发送位置信息
    '''
    每隔60s，将位置信息发送给服务器
    '''
    with open('./n1.txt', 'r') as fp_xy:
        xy_line = fp_xy.readline().rstrip('\n')
        xy_list = xy_line.split('\t')
        position_x = float(xy_list[1])
        position_y = float(xy_list[2])
        position = 'ClientPosition' + '$' + str(position_x) + '$' + str(position_y)
        s.sendall(bytes(str(position), 'utf-8'))
        time.sleep(60)


cycle_time = time.time()  # 获取初始时间

try:
    _thread.start_new_thread(send_position, s)
finally:
    pass

while True:

    size = get_size(FILE_DIR)  # 首先判断存储大小是否超过限定值

    while size > 20:  # 存储上限1G
        print('My files are too lot ,I will ask the basestation how to delete them.')
        send_info = 'HowToDelete'
        s.sendall(bytes(send_info, 'utf-8'))  # 发送请求如何删除
        delete_name = s.recv(1024)   # 被删除的文件名称
        os.remove(FILE_DIR+'/' + delete_name)
        print('I have deleted ', delete_name)
        client_file.remove(delete_name)
        size = get_size(FILE_DIR)

    '''
    开始请求文件
    '''
    print('Please input the file''s name you want:')
    filename = auto_request(client_file, all_files)
    print('I want ', filename)

    # 第一次动态发送，请求文件名
    send_info = 'RequestFile' + '$' + filename
    s.sendall(bytes(filename, "utf-8"))

    # 第一次动态接收，发送端名称
    best_client = str(s.recv(4096), "utf-8")
    print(best_client, 'will send', filename, 'to me.')

    with open(FILE_DIR+'/'+filename, 'w') as f:
        file_data = s.recv(4096)
        f.write(str(file_data, "utf8"))
        print("Successfully get the file !")
        print('------------------------------------------------------')
        client_file.append(filename)      # 更新自身所含文件列表，以免重复请求


    




