import json
import time
import os
import math


def find_the_best_client(clients_with_file, all_client_position, client_name):
    '''
    :param clients_with_file: 拥有所需要的文件的所有客户端列表
    :param all_client_position:所有客户端的位置信息字典
    :param client_name:当前客户端的名称
    :return:最优的客户端
    '''
    if len(clients_with_file) == 0:
            best_client = 'basestation'
            return best_client
    else:
        best_client = clients_with_file[0]
        shortest_distance = pow(all_client_position[best_client][0] - all_client_position[client_name][0], 2) \
                                + pow(all_client_position[best_client][1] - all_client_position[client_name][1], 2)
        for name in clients_with_file:
            if name == best_client:
                continue
            new_distance = pow(all_client_position[name][0] - all_client_position[client_name][0], 2) \
                                + pow(all_client_position[name][1] - all_client_position[client_name][1], 2)
            print('new_distance^2:{}\n shortest_distance^2:{}\n'.format(new_distance, shortest_distance))
            if new_distance <= shortest_distance:
                best_client = name
                shortest_distance = new_distance
    return best_client
