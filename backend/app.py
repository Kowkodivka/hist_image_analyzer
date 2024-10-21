import cv2
import numpy as np
from process import process_images
from typing import List
from fastapi import FastAPI, File, UploadFile


app = FastAPI()


@app.post("/model")
async def model(files: List[UploadFile] = File(...)):
    images = []

    for file in files:
        content_type = file.content_type

        if not content_type.startswith("image/"):
            raise HTTPException(
                status_code=415,
                detail=f"Invalid file type: {content_type}. Acceptable types: image/*.",
            )

        content = await file.read()
        image = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_COLOR)
        images.append(image)

    proc_images = process_images(images)

    return {"message": ":/"}
