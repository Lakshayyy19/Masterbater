from fastapi import FastAPI, UploadFile, File
import uvicorn
from pathlib import Path
from utils.load_model import model
from utils.inference import predict_image
from pydantic import BaseModel
from typing import List, Dict, Optional
from PIL import Image
import io, base64, os, json

# FAST API Endpoint
app = FastAPI()

class ResponseModel(BaseModel):
    result: List[Dict]
    output_image_b64: Optional[str] = None
    json_file: Optional[str] = None

@app.post("/", response_model=ResponseModel)
async def predict_api(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    result = predict_image(image)
    json_result = result["result"]
    output_image = result.get("output_image")
    b64_img = None
    if output_image:
        buf = io.BytesIO()
        output_image.save(buf, format="PNG")
        b64_img = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

    return ResponseModel(result=json_result, output_image_b64=b64_img)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)