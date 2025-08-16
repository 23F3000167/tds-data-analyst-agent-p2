from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Optional
import os
import base64
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import traceback

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/api/")
async def upload_files(
    questions: UploadFile = File(...),
    data: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None)
):
    try:
        # Read files
        questions_bytes = await questions.read()
        data_bytes = await data.read() if data else None
        image_bytes = await image.read() if image else None

        questions_text = questions_bytes.decode("utf-8", errors="ignore")
        data_text = data_bytes.decode("utf-8", errors="ignore") if data_bytes else None

        # Prepare model input
        prompt = f"Answer the following questions based on the provided data:\n\n{questions_text}"
        if data_text:
            prompt += f"\n\nData:\n{data_text}"

        model = genai.GenerativeModel("gemini-2.0-flash")

        contents = [prompt]
        if image_bytes:
            contents.append({
                "mime_type": image.content_type,
                "data": base64.b64encode(image_bytes).decode("utf-8")
            })

        # Call Gemini
        response = model.generate_content(contents)

        return JSONResponse(content={"answers": response.text})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/")
def root():
    return {"message": "Welcome to the Data Analyst Agent API. Use POST /api/ to analyze data."}