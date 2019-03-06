import tesserocr
from PIL import Image


def verify(image):
    '''
    破解验证码图片
    :param image:
    :return: 验证码（识别不了的情况下，可能为空字符串）
    '''
    image.show()
    image = image_gray_deal(image)
    image = image_thresholding_deal(image)
    verifycode = tesserocr.image_to_text(image)

    #无法识别的情况，可能为空字符串
    #print(verifycode, type(verifycode))
    return verifycode

def image_gray_deal(image):
    '''
    灰度处理
    :param image:
    :return:
    '''
    image = image.convert('L')
    #image.show()
    return image

def image_thresholding_deal(image):
    '''
    二值化处理
    :param image:
    :return:
    '''
    threshold = 230
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    #image.show()
    return image

if __name__ == '__main__':
    image = Image.open('../test.png')
    verify(image)