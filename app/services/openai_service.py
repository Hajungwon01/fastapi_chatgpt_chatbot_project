# app/services/openai_service.py

import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from app.schemas import ChatMessage

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def generate_chat_reply(
    message: str,
    history: List[ChatMessage],
    # ── 추가된 설정 파라미터 ──────────────────────────
    system_instruction: str = "너는 한국어로 친절하고 정확하게 답변하는 FastAPI 기반 ChatGPT 챗봇이다.",
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 1.0,
    max_tokens: int = 1024,
    # ────────────────────────────────────────────────
) -> tuple[str, bool]:

    if client is None:
        demo_reply = (
            "현재 OPENAI_API_KEY가 설정되어 있지 않아 데모 모드로 응답합니다. "
            "실제 ChatGPT 답변을 받으려면 프로젝트 루트의 .env 파일에 "
            "OPENAI_API_KEY 값을 설정하세요.\n\n"
            f"입력한 질문: {message}"
        )
        return demo_reply, True

    # ── system instruction을 파라미터로 받아서 사용 ──
    messages = [{"role": "system", "content": system_instruction}]

    for item in history:
        if item.role in {"user", "assistant", "system"}:
            messages.append({"role": item.role, "content": item.content})

    messages.append({"role": "user", "content": message})

    # ── model, temperature, top_p, max_tokens 파라미터 적용 ──
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )

    reply = completion.choices[0].message.content or "응답 내용이 비어 있습니다."
    return reply, False