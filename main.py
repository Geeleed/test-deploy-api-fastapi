# อย่าลืมลากไฟล์ activate.bat ของ virtual env ที่ต้องการมาใส่ terminal ก่อนเพื่อให้ python เราเข้าไปอยู่ในสภาพแวดล้อมนั้น
# ใช้คำสั่งนี้เพื่อเปิดเซิฟเวอร์ uvicorn main:app --port 8001 --reload

from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.get("/")  
async def geeleed():
    return '<Geeleed/> สวัสดีครับ นี่คือ api ที่ใช้ไลบรารี่ FastAPI ของ python ในการทำ คุณสามารถดูว่ามี api อะไรให้ใช้บ้างโดยไปที่ /docs '

@app.get("/{id}/")  # decorator to define a route for GET method on "/{id}" path
async def test(id:str):
    return {"message": f"Hello World {id}"}  # Return a JSON response with the dynamic "id"

# api เข้ารหัสข้อความ sha256
import hashlib
@app.get('/sha256/{text}/')
async def sha256(text:str):
    inst = hashlib.sha256()
    inst.update(text.encode('utf-8'))
    hash_binary = inst.digest()
    hash_hex = hash_binary.hex()
    return hash_hex

# api แปลงเลขฐาน
@app.get('/convert_base/{number}/{from_base}/{to_base}/')
async def convert_base(number,from_base=10,to_base=16):
    keyValue = {
        '0':'0',
        '1':'1',
        '2':'2',
        '3':'3',
        '4':'4',
        '5':'5',
        '6':'6',
        '7':'7',
        '8':'8',
        '9':'9',
        '10':'a',
        '11':'b',
        '12':'c',
        '13':'d',
        '14':'e',
        '15':'f',
        'a':'10',
        'b':'11',
        'c':'12',
        'd':'13',
        'e':'14',
        'f':'15'
        }
    from_base = int(from_base)
    to_base = int(to_base)
    dec = int(str(number),from_base)
    result = ''
    while dec>0:
        remainder = dec%to_base
        result = keyValue[str(remainder)]+result
        dec //= to_base
    return result

# # ขอข้อมูล array ของรูปภาพ
from io import BytesIO
import requests
from PIL import Image
import numpy as np
@app.get('/image2array/{image_url:path}/')
async def image2array(image_url:str):
    response = requests.get(image_url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    image_array = np.asarray(image)
    return {"data":image_array.tolist()}

# รับภาพมาคำนวณสัดส่วนแสงสี
@app.post('/photo-value/')
async def photoValue(file:UploadFile):
    image_data = await file.read()
    img = Image.open(BytesIO(image_data))
    img_array = np.array(img)
    # คำนวณปริมาณของสีแต่ละสีในภาพ
    red_mean = np.mean(img_array[:, :, 0])  # สีแดง
    green_mean = np.mean(img_array[:, :, 1])  # เขียว
    blue_mean = np.mean(img_array[:, :, 2])  # น้ำเงิน
    # คำนวณความสว่างของภาพในช่วง 0-1
    brightness_normalized = np.mean(img_array) / 255.0
    return {
        "red_percentage": (red_mean / 255) * 100,
        "green_percentage": (green_mean / 255) * 100,
        "blue_percentage": (blue_mean / 255) * 100,
        "brightness_normalized": brightness_normalized
    }

def compute_histogram(image_np):
    if image_np.shape[-1] == 3:
        image_gray = np.dot(image_np[...,:3], [0.2989, 0.5870, 0.1140])
    else:
        image_gray = image_np
    hist = np.histogram(image_gray, bins=256, range=(0, 256))[0]
    mean = np.mean(hist)
    sd = np.std(hist)
    skewness = ((hist - mean) ** 3).sum() / (len(hist) * sd ** 3)
    kurtosis = ((hist - mean) ** 4).sum() / (len(hist) * sd ** 4)
    return {
        "mean": mean,
        "sd": sd,
        "skewness": skewness,
        "kurtosis": kurtosis,
        "histogram": hist.tolist()
    }

# วิเคราะห์ histogram ของภาพ
@app.post('/photo-hist-data/')
async def photoHistData(file: UploadFile):
    image_bytes = await file.read()
    image_np = np.array(Image.open(BytesIO(image_bytes)))
    
    result = {
        "grayscale": compute_histogram(image_np),
        "red": compute_histogram(image_np[..., 0]),
        "green": compute_histogram(image_np[..., 1]),
        "blue": compute_histogram(image_np[..., 2])
    }

    return result

# สุ่มตัวเลข
@app.get("/random/{min}/{max}/{num}")
async def randomNumber(min:float,max:float,num:int):
    return np.random.uniform(float(min),float(max),int(num)).tolist()

# การจัดเรียงแบบ permutation
# การจัดเรียงแบบ commutation