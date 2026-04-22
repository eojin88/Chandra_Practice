# %%
# pip install fastapi uvicorn ollama openai python-multipart python-dotenv pillow pymysql cryptography

import os
import base64
import io
from typing import List
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import ollama
from PIL import Image


# %%

# DB 모듈 임포트
import database

# 환경 변수 로드
load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def encodeImageToBase64(imageBytes):
    """ 이미지를 Base64 문자열로 인코딩합니다. """
    return base64.b64encode(imageBytes).decode("utf-8")

@app.post("/analyze")
async def analyzeImage(image: UploadFile = File(...), question: str = Form(...)):
    """ 업로드된 이미지를 분석하고 질문에 답변하며 결과를 DB에 저장합니다. """
    try:
        # 설정 로드
        if not image.content_type.startswith("image/"):
            return {"success": False, "message": "이미지 파일만 업로드 가능합니다."}
        
        useModel = os.getenv("USE_MODEL", "OLLAMA")
        imageContent = await image.read()
        
        resultText = ""
        modelNameForDb = ""
        
        if useModel == "GPT":
            # apiKey 먼저 선언
            apiKey = os.getenv("OPENAI_API_KEY")
            # GPT 모델 사용 로직
            # api키 카드 등록해야하는것 같아서 api키 값 없으면 올라마로 넘어가기
            if not apiKey:
                useModel = "OLLAMA"
            else:    
                modelNameForDb = "gpt-4o"
                client = OpenAI(api_key=apiKey)
                base64Image = encodeImageToBase64(imageContent)
                
                response = client.chat.completions.create(
                    model=modelNameForDb,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": question},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:{image.content_type};base64,{base64Image}"}
                                }
                            ]
                        }
                    ]
                )
                resultText = response.choices[0].message.content
            
        elif useModel == "OLLAMA":
            # Ollama 모델 사용 로직
            modelNameForDb = os.getenv("OLLAMA_MODEL", "gemma4:e2b")
            
            response = ollama.chat(
                model=modelNameForDb,
                messages=[
                    {
                        "role": "user",
                        "content": question,
                        "images": [imageContent]
                    }
                ]
            )
            resultText = response["message"]["content"]
            
        else:
            return {"success": False, "message": "지원하지 않는 모델 설정입니다."}
            
        # DB에 분석 결과 저장
        dbSaved = database.saveAnalysisResult(
            fileName=image.filename,
            question=question,
            answer=resultText,
            modelName=modelNameForDb
        )
        
        return {
            "success": True, 
            "data": resultText, 
            "dbSaved": dbSaved
        }
        
    except Exception as e:
        return {"success": False, "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



