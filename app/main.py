# app/main.py

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ChatRequest, ChatResponse
from app.services.openai_service import generate_chat_reply

app = FastAPI(
    title="FastAPI ChatGPT ChatBot",
    description="제공된 React 챗봇 예제를 참고하여 FastAPI와 순수 HTML/JS로 다시 구현한 ChatGPT 챗봇 앱입니다.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR   = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=FileResponse)
def read_index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health_check() -> dict:
    return {"status": "ok", "message": "FastAPI ChatGPT chatbot server is running."}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        # ── 설정값을 서비스 함수에 전달 ──────────────────────
        reply, used_demo_mode = generate_chat_reply(
            message=request.message,
            history=request.history,
            system_instruction=request.system_instruction,
            model=request.model,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
        )
        # ────────────────────────────────────────────────────
        return ChatResponse(reply=reply, used_demo_mode=used_demo_mode)

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"챗봇 응답 생성 중 오류가 발생했습니다: {exc}") from exc