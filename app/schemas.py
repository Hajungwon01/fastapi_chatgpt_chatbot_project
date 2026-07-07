# app/schemas.py

from typing import List
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(
        ...,
        description="메시지 역할: system, user, assistant 중 하나",
        examples=["user"],
    )
    content: str = Field(
        ...,
        min_length=1,
        description="메시지 본문",
        examples=["FastAPI가 무엇인가요?"],
    )


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="사용자가 입력한 새 질문",
        examples=["파이썬 FastAPI의 장점을 알려줘"],
    )
    history: List[ChatMessage] = Field(
        default_factory=list,
        description="이전 대화 내역",
    )

    # ── 추가된 설정 필드 ──────────────────────────────────────
    system_instruction: str = Field(
        default="너는 한국어로 친절하고 정확하게 답변하는 FastAPI 기반 ChatGPT 챗봇이다.",
        description="System Instruction",
    )
    model: str = Field(
        default="gpt-4o-mini",
        description="사용할 OpenAI 모델명",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature (0~2)",
    )
    top_p: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Top P (0~1)",
    )
    max_tokens: int = Field(
        default=1024,
        ge=64,
        le=4096,
        description="최대 출력 토큰 수",
    )
    # ────────────────────────────────────────────────────────


class ChatResponse(BaseModel):
    reply: str = Field(
        ...,
        description="챗봇 답변",
        examples=["FastAPI는 파이썬 기반의 빠른 웹 API 프레임워크입니다."],
    )
    used_demo_mode: bool = Field(
        default=False,
        description="OPENAI_API_KEY가 없어서 데모 응답을 사용했는지 여부",
    )