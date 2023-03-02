#!python3
# -*- coding:utf8 -*-

import numpy as np
b = np.ones((3, 4), dtype=np.int64)
# [[1 1 1 1]
#  [1 1 1 1]
#  [1 1 1 1]]
print(b)

print("b shape:", b.shape)

a = np.array([[1, 5, 5, 2],
              [9, 6, 2, 8],
              [3, 7, 9, 1]])

print("a shape:", a.shape)

# 每列最大值下标,[1 2 2 1]
print("argmax axis=0", np.argmax(a, axis=0))

# 每列最大值下标,[9 7 9 8]
print("max axis=0", np.max(a, axis=0))

# 每行最大值下标,[1 0 2]
print("argmax axis=1", np.argmax(a, axis=1))

# 每行最大值下标,[5 9 9]
print("max axis=1", np.max(a, axis=1))


a = np.array([1, 2, 3])
b = np.array([11, 22, 33])
c = np.array([44, 55, 66])
# 有效的数组拼接
abc = np.concatenate((a, b, c), axis=0)
print("abc shape:", abc)

a = np.array([[1, 5, 5, 2],
              [9, 6, 2, 8],
              [3, 7, 9, 1]])

# 用于将数组的元素沿指定的轴旋转90度
a_rot = np.rot90(a)
print("a_rot:", a_rot)
