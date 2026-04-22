# AI 프로젝트개발표준가이드(Model Serving)

## 1. 기본원칙
-**언어:** 모든답변및주석은**한국어** (코드는영문).
-**톤:** 친절하고전문적인IT 교육자톤유지.
-**환경:** Python 3.12.10 필수.

## 2. 핵심아키텍처및모델스위칭
-**Model Selector:** `config.py` 또는환경변수를통해`GPT`와`OLLAMA` 모드를전환할수있어야함.
-**Ollama 설정:** 로컬GPU를활용하며`gemma4:e2b` 모델을기본으로사용.
-**Stateless 구조:** API는요청마다독립적으로처리하며, 데이터는MySQL에영구저장.

## 3. 프로젝트구조(ai_project)
/ai_project
├── app.ipynb (FastAPI 실행)
├── .env(GPT/Ollama 설정및API Key 관리)
├── database.py (MySQL 연동및쿼리관리)
├── dataset/ (이미지및학습데이터저장소)
└── AI_GUIDE.md (현재가이드파일)

## 4. 코딩스타일(Strict)
-**명명규칙:** 변수명과함수명은`camelCase` 사용.
-**반복문:** 리스트컴프리헨션사용금지. 반드시`for i in range(0, len(obj)):` 형식을취할것.
-**조건문:** `if-elif-else`를명확히구분하여작성.
-**함수:** 모든함수는`def funcName(param):` 뒤에`""" 함수설명"""`을필수로작성.
-**파일경로:** `os.path` 대신`os.listdir`와경로조작함수를적절히혼용하여관리.

## 5. 보안및에러처리
-**CORS:** 모든Origin/Method/Header 허용(`*`).
-**예외처리:** 전체로직을`try-except`로감싸고, 에러발생시아래JSON 반환.
-형식: `{"success": false, "message": "에러내용"}`