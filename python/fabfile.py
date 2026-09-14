#!python3
# -*- coding:utf8 -*-

# fab默认采用fabfile.py作为入口代码脚本,否则就要指定 -f xxx.py
# task函数名不要用下划线,否则task名称会改变

# pip3 install fabric2
# pip3 install pyyaml


from fabric import task
from fabric import Connection

cur_remote_data_path = "/root/"
cur_remote_conn = Connection(
    "root@ip",
)


def upload(file_list):
    global cur_remote_conn, cur_remote_data_path

    assert cur_remote_conn, "远程主机为空"
    assert cur_remote_data_path, "远程数据路径为空"

    for file in file_list:
        print(file, "put over")

    for file in file_list:
        cur_remote_conn.put(file, cur_remote_data_path)
        print(file, "put over")


@task
def download(c):
    global cur_remote_conn
    assert cur_remote_conn, "远程主机为空"

    # 下载日志
    cur_remote_conn.get("index.html")
