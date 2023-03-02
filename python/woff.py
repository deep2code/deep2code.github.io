from fontTools.ttLib import TTFont

import os
import shutil
from fontTools.pens.svgPathPen import SVGPathPen
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import io


def woff_to_pngdir(woff_file):
    base_file_name = os.path.splitext(woff_file)[0]
    if os.path.exists(base_file_name):
        # 删除非空目录
        shutil.rmtree(base_file_name, ignore_errors=True)

    try:
        os.mkdir(base_file_name)
    except Exception as e:
        print(e)

    # 读取woff文件
    font = TTFont(woff_file)
    charsdict = font.getBestCmap()

    for key, value in charsdict.items():
        # 产生svg
        pen = SVGPathPen(font.getGlyphSet())
        font.getGlyphSet()[value].draw(pen)
        xMin, xMax, yMin, yMax = (
            font["head"].xMin,
            font["head"].xMax,
            font["head"].yMin,
            font["head"].yMax,
        )
        height = yMax - yMin
        width = xMax - xMin
        # r=width/100
        svg_xml = f'<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="{xMin} {yMin} {width} {height}"><g transform="matrix(0.6 0 0 -0.6 {xMin+width*0.2} {yMin+yMax-height*0.2})"><path stroke = "black" fill = "black" d="{pen.getCommands()}"/></g></svg>'

        # 内存png
        drawing = svg2rlg(io.StringIO(svg_xml))

        # 保存识别结果
        renderPM.drawToFile(drawing, rf"{key}-{value}.png")


if __name__ == "__main__":
    woff_to_pngdir("abc.woff")
