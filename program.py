import requests
from PIL import Image
from io import BytesIO
import numpy as np

# URL ของรูปภาพ
# image_url = "https://aipp.silverchair-cdn.com/data/SiteBuilderAssetsOriginals/Live/Images/aapt/logo.png"
image_url = "https://lzd-img-global.slatic.net/g/p/32d176317d0ede4eae337749487ec6e7.jpg_720x720q80.jpg"

# ดาวน์โหลดรูปภาพจาก URL
response = requests.get(image_url)
image_data = response.content

# แปลงข้อมูลรูปภาพในรูปแบบ bytes เป็นภาพ
image = Image.open(BytesIO(image_data))

# แสดงภาพ
# image.show()

image_array = np.asarray(image)
print(image_array)
print(np.mean(image_array,axis=3))

# def image2array(image_url:str):
#     response = requests.get(image_url)
#     image_data = response.content
#     image = Image.open(BytesIO(image_data))
#     image_array = np.asarray(image)
#     return image_array

# print(image2array('https://png.pngtree.com/png-clipart/20190116/ourmid/pngtree-hand-painted-dolphins-cartoon-dolphin-q-version-of-dolphin-lovely-png-image_387165.jpg'))