'''
该项目修改思想：
将介于client与server之间的固定的通信流程修改为：
1、server不会无故向client发送消息
2、每个client与server之间初始建立连接时会初始化传递一些变量（此处通信流程为固定）
3、client向server发送消息类型暂时分为三类：ClientPosition,HowToDelete,RequestFile
    server对收到的信息类型进行判断，并作出相应行为（每类消息中的通信流程为固定）
'''

import socketserver
import json
import time
import os
from .file_system import get_all_file
from .position_system import find_the_best_client
from .log_system import write_log
from .command_system import request_file, client_position

i = 0                                 # 标识Client
DATA = {}                             # 所有客户端所拥有的文件名
start_time = time.time()
all_client_position = {}
FILE_DIR = os.getcwd()+'/server_dir'  # 存储所有的文件夹所在的位置
all_files = get_all_file(FILE_DIR)    # 所有客户端所拥有的文件的字典


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global i
        global DATA
        global all_client_position
        client_name = 'C' + str(i)  # 最新连接的客户端代号，如C1 , C2
        print(client_name)

        # 第一次发送,发送客户端名称
        self.request.sendall(bytes(client_name, encoding="utf8"))
        i += 1
        print('get connection from', self.client_address, 'as', client_name)

        # 第二次发送，将all_files发给客户端
        self.request.sendto(json.dumps(all_files).encode(), (h, p))

        # 第一次接收，客户端初始化的文件
        received_info = self.request.recv(1024)
        client_file = json.loads(str(received_info, encoding='utf-8'))
        DATA[client_name] = tuple(client_file)

        while 1:

            # 接收
            received_info = self.request.recv(1024)
            split_command = str(received_info, encoding='utf-8').split('$')

            # # OwnFiles表示接收到Client所含有的文件
            # if split_command[0] == 'OwnFiles':
            #     DATA = own_files(split_command, client_name, DATA)
            #     send_info = 'Pass'
            #     self.request.sendall(bytes(str(send_info), encoding="utf8"))
            #     continue

            # 接收到Client的位置信息
            if split_command[0] == 'ClientPosition':
                all_client_position = client_position(split_command, all_client_position, client_name)
                continue

            if split_command[0] == 'HowToDelete':
                '''
                此处调用强化学习算法，并发送相应删除命令
                '''
                pass

            # 接收到Client的文件请求信息
            if split_command[0] == 'RequestFile':
                clients_with_file, filename = request_file(split_command, client_name, DATA)
                best_client = find_the_best_client(clients_with_file, all_client_position, client_name)
                send_info = best_client
                self.request.sendall(bytes(str(send_info), encoding="utf8"))
                print(best_client, 'is the best client.')
                with open(FILE_DIR + '/' + filename, 'r') as f:
                    file_data = f.read()
                    self.request.sendall(bytes(file_data, encoding="utf8"))
                    DATA[client_name] = DATA[client_name] + tuple([filename])
                    write_log(best_client, client_name, filename, all_client_position, start_time)
                    print(best_client, 'has send', filename, 'to', self.client_address, client_name)
                    print('------------------------------------------------------')
                continue


if __name__ == '__main__':
    h, p = '0.0.0.0', 9999
    server = socketserver.ThreadingTCPServer((h, p), MyTCPHandler)
    server.serve_forever()
