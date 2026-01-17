import json
import logging
from typing import List, Optional

from pydantic import BaseModel, ValidationError

logger = logging.getLogger("app.ai.report")


class Slide(BaseModel):
    title: str
    content: str


class Deck(BaseModel):
    slides: List[Slide]


class PPTReportGenerator:
    def __init__(self, ai_service):
        self.ai_service = ai_service

    def _build_prompt(self, user_data: str) -> str:
        return f"""
당신은 금융 분석가입니다.
아래 데이터를 바탕으로 PPT 슬라이드 내용을 JSON으로만 출력하세요.

[DATA_BEGIN]
{user_data}
[DATA_END]

반드시 아래 스키마를 따르세요:
{{"slides":[{{"title":"...", "content":"..."}}]}}

JSON 외의 텍스트는 절대 출력하지 마세요.
""".strip()

    async def generate_ppt_data(self, user_data: str) -> dict:
        prompt = self._build_prompt(user_data)

        raw = await self.ai_service.get_response(prompt)
        deck = self._parse_and_validate(raw)
        if deck:
            return deck.model_dump()

        logger.warning("ai_format_mismatch -> repair_retry")
        repair_prompt = f"""
다음 출력은 JSON 형식이 깨졌습니다.
오직 JSON만 반환하도록 수정하세요. JSON 외 텍스트 금지.

[RAW_BEGIN]
{raw}
[RAW_END]
""".strip()

        raw2 = await self.ai_service.get_response(repair_prompt)
        deck2 = self._parse_and_validate(raw2)
        if deck2:
            return deck2.model_dump()

        return {"slides": [{"title": "Error", "content": "Format Error"}]}

    def _parse_and_validate(self, raw: str) -> Optional[Deck]:
        try:
            data = json.loads(raw)
            return Deck.model_validate(data)
        except (json.JSONDecodeError, ValidationError):
            return None