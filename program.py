import requests
from PIL import Image
from io import BytesIO
import numpy as np

# URL ของรูปภาพ
image_url = "https://aipp.silverchair-cdn.com/data/SiteBuilderAssetsOriginals/Live/Images/aapt/logo.png"

# ดาวน์โหลดรูปภาพจาก URL
response = requests.get(image_url)
image_data = response.content

# แปลงข้อมูลรูปภาพในรูปแบบ bytes เป็นภาพ
image = Image.open(BytesIO(image_data))

# แสดงภาพ
# image.show()

image_array = np.asarray(image)
print(image_array)