"""
Vehicle License Plate Recognition API

This FastAPI application exposes an endpoint (`/api/identify`) that accepts a POST
request containing an image in base64 or data URL format.cThe image is processed using
an Automatic License Plate Recognition (ALPR) model to detect and extract the license
plate number.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from utils import process_image

app = FastAPI()


@app.post("/api/identify")
async def handle_identify(request: Request):
    """
    Handle the license plate identification endpoint.

    Args:
        request (Request): HTTP request containing a JSON body with the key "image_url"

    Returns:
        JSONResponse:
            - 200 OK: A JSON object with license plate information if detection is successful.
            - 400 Bad Request: If the "image_url" field is missing.
            - 404 Not Found: If no license plate is detected in the image.
    """
    data = await request.json()
    image_url = data.get("image_url")
    if not image_url:
        return JSONResponse(
            status_code=400, content={"error": "Thiếu trường image_url"}
        )
    if not (response := process_image(image_url)):
        return JSONResponse(
            status_code=404, content={"error": "Không tìm thấy biển số xe"}
        )
    return response
