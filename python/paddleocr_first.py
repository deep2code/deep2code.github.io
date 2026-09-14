#!python3
import re
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
# need to run only once to download and load model into memory
ocr = PaddleOCR(use_angle_cls=False, lang="ch", show_log=False)
img_path = '01.jpg'
result = ocr.ocr(img_path, cls=False)
# for line in result:
#     for box in line:
#         print(type(box), box)
#     break

result = result[0]
# 显示结果

image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
boxes = [result[0]]
txts = [result[1][0]]
scores = [result[1][1]]
im_show = draw_ocr(image, boxes, txts, scores, font_path='simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')
