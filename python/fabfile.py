#!/usr/bin/env python
# -*- coding:utf8 -*-

# fab默认采用fabfile.py作为入口代码脚本,否则就要指定 -f xxx.py
# task函数名不要用下划线,否则task名称会改变

# pip3 install fabric2
# pip3 install pyyaml

# 调用执行示例
# fab remote pre yearall
# fab remote pre prov 31 provall


from fabric import task
from fabric import Connection
import yaml

cur_year = 2022


@task
def year(c, y):
    global cur_year
    cur_year = y

    print(cur_year)


cur_province = None


@task
def prov(c, p):
    global cur_province
    cur_province = p

    print(cur_province)


with open('server.yaml', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    local_data_path = config['storage']['local']['path']

cur_remote_data_path = None
cur_remote_conn = None


@task
def remote(c, dest):
    assert dest in ['pre', 'pro'], print('未知远程主机', dest)

    jump_privatekey_file = 'jump_id_rsa'

    import os
    assert os.path.exists(jump_privatekey_file), print(
        jump_privatekey_file, '不存在')

    global cur_remote_data_path
    if dest == "pre":
        # data-1
        remote_host_config = 'admin@172.21.245.211'
        cur_remote_data_path = '/nfs/conf/gaokao-data/'
    elif dest == "pro":
        # pro-k8s-01
        remote_host_config = 'admin@172.16.190.152'
        cur_remote_data_path = '/mnt/gaokao-data/'

    print(remote_host_config)

    global cur_remote_conn
    cur_remote_conn = Connection(
        remote_host_config,
        connect_kwargs={'key_filename': jump_privatekey_file},
        gateway=Connection('admin@121.40.55.65'),
    )


def confirm_remote(c):
    global cur_remote_conn

    if cur_remote_conn is None:
        remote(c, 'pre')


def cmp_file_suffix(left, right):
    import os
    left_suffix = os.path.splitext(left)[-1]
    right_suffix = os.path.splitext(right)[-1]

    # 复制顺序,否则造成数据不会更新或错乱
    order_list = ['data', 'meta', 'version']

    left_pos = -1
    if left_suffix in order_list:
        left_pos = order_list.index(left_suffix)

    right_pos = -1
    if right_suffix in order_list:
        right_pos = order_list.index(right_suffix)

    return left_pos < right_pos


def upload(file_list):
    global cur_remote_conn, cur_remote_data_path

    assert cur_remote_conn, '远程主机为空'
    assert cur_remote_data_path, '远程数据路径为空'

    import functools
    file_list.sort(key=functools.cmp_to_key(cmp_file_suffix))

    for file in file_list:
        print(file, 'put over')

    for file in file_list:
        cur_remote_conn.put(file, cur_remote_data_path)
        print(file, 'put over')


@task
def yearpublic(c):
    global cur_year, local_data_path
    assert cur_year, '年份为空'
    assert local_data_path, '本地数据路径为空'

    confirm_remote(c)

    file_list = [
        "schCelebrity", "schEnrollRule", "schRank", "schRankType",
        "schSku", "similarMajor", "similarSch", "majorSku", "majorCareer",
    ]
    upload_file_list = []

    for flie in file_list:
        upload_file_list.append(
            local_data_path+"/{}-{}--.data".format(cur_year, flie),
        )
        upload_file_list.append(
            local_data_path+"/{}-{}--.meta".format(cur_year, flie),
        )

    upload(upload_file_list)


@task
def yearall(c):
    global cur_year, local_data_path
    assert cur_year, '年份为空'
    assert local_data_path, '本地数据路径为空'

    confirm_remote(c)

    import glob
    upload(glob.glob(local_data_path+'/{}*'.format(cur_year)))


@task
def provall(c):
    global cur_year, cur_province, local_data_path
    assert cur_year, '年份为空'
    assert cur_province, '省份为空'
    assert local_data_path, '本地数据路径为空'

    confirm_remote(c)

    import glob
    file_list = glob.glob(
        local_data_path+'/{}*{}0000000000*'.format(cur_year, cur_province),
    )

    upload(file_list)


@task
def log(c):
    confirm_remote(c)

    global cur_remote_conn
    assert cur_remote_conn, '远程主机为空'

    # 下载日志
    cur_remote_conn.get('/home/admin/ds/data-service.log', local='remote.log')


@task
def exe(c):
    confirm_remote(c)

    global cur_remote_conn
    assert cur_remote_conn, '远程主机为空'

    # 上传exe
    remote_path = '/home/admin/ds'
    exe_name = 'data-service'

    cur_remote_conn.run('killall {}'.format(exe_name), warn=True)
    cur_remote_conn.put(exe_name, remote_path)
    cur_remote_conn.run('chmod +x {}/{}'.format(remote_path, exe_name))


@task
def download(c):
    confirm_remote(c)

    global cur_remote_conn, cur_remote_data_path
    assert cur_remote_conn, '远程主机为空'

    # import os
    # # 下载相关文件
    # with open('31.log', encoding='utf-8') as f:
    #     for line in f:
    #         fileName = line.strip()
    #         cur_remote_conn.get(cur_remote_data_path+fileName, local=os.path.join(local_data_path, fileName))

    # # 临时调试用
    # # 下载相关文件
    # # remote_path = '/home/admin/ds/31.log'
    # # cur_remote_conn.get(remote_path)

    # global local_data_path,cur_remote_data_path
    # assert local_data_path, '本地数据路径为空'
    # assert cur_remote_data_path, '远程数据路径为空'

    # import os
    # # 下载相关文件
    # with open('31.log', encoding='utf-8') as f:
    #     for line in f:
    #         fileName = line.strip()
    #         cur_remote_conn.get(cur_remote_data_path+fileName, local=os.path.join(local_data_path, fileName))
