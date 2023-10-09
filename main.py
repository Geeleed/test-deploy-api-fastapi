from fastapi import FastAPI
# from starlette.responses import StreamingResponse
from starlette.responses import FileResponse
import requests
import tempfile

app = FastAPI()

@app.get("/")  
async def root(): 
    return {"message": "Hello World"} 

@app.get("/{id}")  # decorator to define a route for GET method on "/{id}" path
async def root(id:str):
    return {"message": f"Hello World {id}"}  # Return a JSON response with the dynamic "id"

# # API ดาวน์โหลดรูปภาพจาก URL
# @app.get("/download/{image_url:path}")
# async def download_image(image_url: str):
#     # ดาวน์โหลดรูปภาพจาก URL
#     response = requests.get(image_url, stream=True)
    
#     # ตรวจสอบว่าการดาวน์โหลดเสร็จสิ้นและสำเร็จ
#     if response.status_code == 200:
#         # สร้างการตอบสนอง StreamingResponse โดยใช้ response.iter_content เพื่อส่งข้อมูลไปยังการตอบสนองในรูปแบบ Streaming
#         headers = {"Content-Disposition": f"attachment; filename=downloaded_image.jpg"}  # ระบุชื่อไฟล์ที่ต้องการให้ผู้ใช้ดาวน์โหลด
#         return StreamingResponse(iter(response.iter_content(chunk_size=128)), media_type="image/jpeg", headers=headers)
#     else:
#         # หากไม่สามารถดาวน์โหลดรูปภาพได้
#         return {"error": "Unable to download image"}


app = FastAPI()

# API ดาวน์โหลดรูปภาพจาก URL
@app.get("/download/{image_url:path}")
async def download_image(image_url: str):
    # ดาวน์โหลดรูปภาพจาก URL
    response = requests.get(image_url, stream=True)
    
    # ตรวจสอบว่าการดาวน์โหลดเสร็จสิ้นและสำเร็จ
    if response.status_code == 200:
        # สร้างไฟล์ชั่วคราวเพื่อเก็บข้อมูลรูปภาพ
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in response.iter_content(chunk_size=128):
                temp_file.write(chunk)
        
        # สร้างการตอบสนอง FileResponse โดยระบุชื่อไฟล์ที่ต้องการให้ผู้ใช้ดาวน์โหลด
        file_name = "downloaded_image.jpg"  # ระบุชื่อไฟล์ที่ต้องการให้ผู้ใช้ดาวน์โหลด
        return FileResponse(temp_file.name, headers={"Content-Disposition": f"attachment; filename={file_name}"})
    else:
        # หากไม่สามารถดาวน์โหลดรูปภาพได้
        return {"error": "Unable to download image"}


# uvicorn api:app --port 8001 --reload

