from fastapi import FastAPI
from starlette.responses import StreamingResponse
import requests

app = FastAPI()

@app.get("/")  
async def root(): 
    return {"message": "Hello World"} 

@app.get("/{id}")  # decorator to define a route for GET method on "/{id}" path
async def root(id:str):
    return {"message": f"Hello World {id}"}  # Return a JSON response with the dynamic "id"

# downloadFileFromUrl.py
@app.get("/download/{image_url:path}")
async def download_image(image_url: str):
    # ดาวน์โหลดรูปภาพจาก URL
    response = requests.get(image_url, stream=True)
    
    # ตรวจสอบว่าการดาวน์โหลดเสร็จสิ้นและสำเร็จ
    if response.status_code == 200:
        # สร้างการตอบสนองเป็น StreamingResponse และส่งข้อมูลไปยังการตอบสนอง
        return StreamingResponse(iter(response.iter_content(chunk_size=128)), media_type="image/jpeg")
    else:
        # หากไม่สามารถดาวน์โหลดรูปภาพได้
        return {"error": "Unable to download image"}


# uvicorn api:app --port 8001 --reload