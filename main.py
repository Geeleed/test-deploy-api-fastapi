from fastapi import FastAPI
app = FastAPI()

@app.get("/")  
async def root(): 
    return {"message": "Hello World"} 

@app.get("/{id}")  # decorator to define a route for GET method on "/{id}" path
async def root(id:str):
    return {"message": f"Hello World {id}"}  # Return a JSON response with the dynamic "id"

# uvicorn api:app --port 8001 --reload