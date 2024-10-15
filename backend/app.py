import cv2
import numpy as np

from process import process_images
from model import images_to_vox
from typing import List
from fastapi import FastAPI, File, UploadFile


app = FastAPI()

# find /home/kowkodivka/Документы/hist_image_analyzer/photo/raw -type f -print0 | xargs -0 -I {} curl -X POST -F "files=@{}" http://127.0.0.1:8000/model

@app.post('/model')
async def model(files: List[UploadFile] = File(...)):
    images = []

    for file in files:
        content_type = file.content_type

        if not content_type.startswith('image/'):
            raise HTTPException(
                status_code=415,
                detail=f"Invalid file type: {content_type}. Acceptable types: image/*."
            )
        
        content = await file.read()
        image = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_COLOR)
        images.append(image)

    proc_images = process_images(images)
    model = images_to_vox(proc_images)

    return {"message": f"{model}"}