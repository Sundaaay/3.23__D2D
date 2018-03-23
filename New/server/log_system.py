import time
import os


def write_log(source_host, target_host, filename, all_client_position, start_time):
    with open(os.getcwd()+'/history', 'a') as f:
        sys_time = str(time.time() - start_time)
        f.write('time:{}\tsource_host{}:{}\ttarget_host{}:{}\ttrans_file:{}\t\n'.format(
            sys_time
            , all_client_position[source_host]
            , source_host
            , all_client_position[target_host]
            , target_host
            , filename))
