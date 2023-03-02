# -*- coding: utf-8 -*-

# pip install -r requirement.txt
# pip install alibabacloud_ocr_api20210707==1.1.8
import json
from logging import exception

from alibabacloud_ocr_api20210707.client import Client as ocr_api20210707Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ocr_api20210707 import models as ocr_api_20210707_models
from alibabacloud_tea_util import models as util_models

# https://help.aliyun.com/document_detail/331008.html
# https://ocr.console.aliyun.com/overview?spm=5176.12127803.J_5253785160.2.4f767813QmL9ES
# 每个月免费200次,后付费类型
def aliyun(img_url):
    config = open_api_models.Config(
        # 您的 AccessKey ID,
        access_key_id="xxxx",
        # 您的 AccessKey Secret,
        access_key_secret="yyyy",
    )
    # 访问的域名
    config.endpoint = "ocr-api.cn-hangzhou.aliyuncs.com"
    client = ocr_api20210707Client(config)

    recognize_general_request = ocr_api_20210707_models.RecognizeGeneralRequest(
        url=img_url
    )
    runtime = util_models.RuntimeOptions()
    try:
        # 复制代码运行请自行打印 API 的返回值
        resp = client.recognize_general_with_options(
            recognize_general_request, runtime
        ).to_map()
        data_json = json.loads(resp["body"]["Data"])
        return data_json["content"]
    except Exception as error:
        return str(error)


# pip install tencentcloud-sdk-python=3.0.720

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.ocr.v20181119 import ocr_client, models

# 免费额度，每月1000次
# https://console.cloud.tencent.com/ocr/stats
def tencent(img_url):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取

        cred = credential.Credential(
            "aaaa",
            "vvvvv",
        )
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ocr_client.OcrClient(cred, "ap-hongkong", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.GeneralBasicOCRRequest()
        params = {"ImageUrl": img_url}
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个GeneralBasicOCRResponse的实例，与请求对象对应
        resp = client.GeneralBasicOCR(req)
        text_list = []
        for td in resp.TextDetections:
            text_list.append(td.DetectedText)
        return "".join(text_list)

    except TencentCloudSDKException as err:
        return str(err)


import _thread
import random


def img_to_text(img_url):
    handle = aliyun
    if random.randint(0, 3) > 0:
        handle = tencent
    try:
        _thread.start_new_thread(handle, (img_url))
        return handle.__name__
    except exception as e:
        print(str(e))


if __name__ == "__main__":
    img_to_text("abc")
    # tencent(
    #     "http://mmbiz.qpic.cn/mmbiz_jpg/orWialEIuwfvLgnHX8t8sXpMqWlsvsSW5E8KtF985vlVxRfFX5aq0ckQnWOAeYMF1Oo7wUMqfu7oCe76v3zT2kw/0"
    # )
