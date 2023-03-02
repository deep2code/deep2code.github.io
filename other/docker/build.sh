#!/bin/sh

docker stop $(docker ps -q)

docker rm $(docker ps -a -q)

#已经停止的，正在运行的不能删除
docker image rm deep2code:v1

# 文件名固定为dockerfile，否则docker build -f指定文件
# build时首次或出现Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them这么一个提示
# 使用"docker 扫描"对映像运行 Snyk 测试
docker build -t deep2code:v1 .
