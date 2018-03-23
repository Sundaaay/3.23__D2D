import os


# def own_files(split_command, client_name, data):
#     '''
#
#     :param split_command:
#     :param client_name:
#     :param data: the files that all clients connected have
#     :return: "data" and "sending command"
#     Example:
#     OwnFiles$file1.txt$file2.txt$file3.txt
#     '''
#
#     client_file = []
#     for temp in range(1, len(split_command)):
#         client_file.append(split_command[temp])
#     data[client_name] = tuple(client_file)
#     print('{} have {}'.format(client_name, client_file))
#     return data


def client_position(split_command, all_client_position, client_name):
    position_x = float(split_command[1])
    position_y = float(split_command[2])
    all_client_position[client_name] = [position_x, position_y]
    return all_client_position



def request_file(split_command, client_name, data):
    '''
    :param split_command: 
    :param client_name: 
    :param data: 
    :return: 
    Example:
    RequestFile$file1.txt
    '''
    clients_with_file = []
    filename = split_command[1]
    all_client = list(data.keys())
    for m in range(len(all_client)):
        for n in range(len(data[all_client[m]])):
            if all_client[m] == client_name:
                continue
            if data[all_client[m]][n] == filename:
                clients_with_file.append(all_client[m])
    return clients_with_file, filename







