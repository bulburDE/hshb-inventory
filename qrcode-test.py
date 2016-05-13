# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# from PIL import Image
import qrcode
import qrcode.image.svg

factory = qrcode.image.svg.SvgPathFillImage

img = qrcode.make('http://hshb.de/g0001', image_factory=factory)

img.save('test.svg')
