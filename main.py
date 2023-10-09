from fastapi import FastAPI
from starlette.responses import StreamingResponse
import requests
import tempfile

app = FastAPI()

@app.get("/")  
async def root(): 
    return {"message": "Hello World"} 

@app.get("/{id}")  # decorator to define a route for GET method on "/{id}" path
async def root(id:str):
    return {"message": f"Hello World {id}"}  # Return a JSON response with the dynamic "id"

# api ดาวน์โหลดรูปภาพจาก URL
@app.get("/download/{image_url:path}")
async def download_image(image_url: str):
    # ดาวน์โหลดรูปภาพจาก URL
    response = requests.get(image_url, stream=True)
    
    # ตรวจสอบว่าการดาวน์โหลดเสร็จสิ้นและสำเร็จ
    if response.status_code == 200:
        # สร้างไฟล์ชั่วคราวเพื่อเก็บข้อมูลรูปภาพ
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            for chunk in response.iter_content(chunk_size=128):
                temp_file.write(chunk)
        
        # สร้างการตอบสนอง StreamingResponse โดยใช้ไฟล์ชั่วคราวที่สร้าง
        file_name = "downloaded_image.jpg"  # ตั้งชื่อไฟล์ตามที่คุณต้องการ
        headers = {"Content-Disposition": f"attachment; filename={file_name}"}
        with open(temp_file.name, "rb") as file:
            return StreamingResponse(iter([file.read()]), media_type="image/jpeg", headers=headers)
    else:
        # หากไม่สามารถดาวน์โหลดรูปภาพได้
        return {"error": "Unable to download image"}


# uvicorn api:app --port 8001 --reload

