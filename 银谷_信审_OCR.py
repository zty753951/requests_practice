# -*- coding: utf-8 -*-

# #作者微信：2501902696
# from PIL import Image
# import pytesseract
# #上面都是导包，只需要下面这一行就能实现图片文字识别
# text=pytesseract.image_to_string(Image.open(r'D:\2.jpg'),lang='chi_sim')
# print(text)



from aip import AipOcr
import json

# 定义常量
APP_ID = '11209335'
API_KEY = '2CBvGIovTxaB22046iIEthvH'
SECRET_KEY = '58PYeQ6bKYErFvKs6ioydOQE2dORSW02 '

# 初始化AipFace对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
filePath = r"D:/identifying_code_img/identifiedcode.jpg"


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

        # 定义参数变量


options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

# 调用通用文字识别接口
result = aipOcr.basicGeneral(get_file_content(filePath), options)


# print(result.get('words_result')[0].get('words'))


word=result.get('words_result')[0].get('words')

# print(word[0:1])
# print(word[1:2])
# print(word[2:3])


if word[1:2]=='+':
    value=int(word[0:1])+int(word[2:3])
    print(value)
elif word[1:2]=='X' or word[1:2]=='x':
    value = int(word[0:1]) * int(word[2:3])
    print(value)

