#!python3
# -*- coding:utf8 -*-

import cv2
import numpy as np

img = cv2.imread("01.jpg", cv2.IMREAD_COLOR)
img_org = img.copy()

print("img shape", img.shape, cv2.IMREAD_COLOR, cv2.COLOR_GRAY2BGR)

# 得到图片的高和宽
img_height, img_width = img.shape[:2]

# 定义对应的点
points1 = np.float32([[75, 55], [340, 55], [33, 435], [400, 433]])
points2 = np.float32([[0, 0], [360, 0], [0, 420], [360, 420]])

# 计算得到转换矩阵
M = cv2.getPerspectiveTransform(points1, points2)

# 实现透视变换转换
processed = cv2.warpPerspective(img, M, (360, 420))

# 读取灰度图片,转彩色
img_gray = cv2.imread("01.jpg", 0)
img_gray_rgb = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

# 显示原图和处理后的图像
cv2.imshow("org", img_org)
cv2.imshow("processed", processed)
cv2.imshow("img_gray_rgb", img_gray_rgb)

cv2.waitKey(0)
