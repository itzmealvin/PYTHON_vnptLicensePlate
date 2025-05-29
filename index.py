from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from utils.utils import process_image

app = FastAPI()


@app.post("/api/identify")
async def handle_identify(request: Request):
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
