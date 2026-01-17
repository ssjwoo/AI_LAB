from app.core.settings import Settings
from app.ai.providers import BasicProvider, FlakyGroundingProvider
from app.ai.breaker import CircuitBreaker
from app.ai.service import AIService
from app.ai.report import PPTReportGenerator


async def demo_ai(settings: Settings):
    grounding = FlakyGroundingProvider(fail_every=2)
    basic = BasicProvider()
    breaker = CircuitBreaker(
        fail_threshold=settings.CB_FAIL_THRESHOLD,
        reset_timeout_sec=settings.CB_RESET_TIMEOUT_SEC,
    )

    service = AIService(
        grounding=grounding,
        basic=basic,
        breaker=breaker,
        use_grounding=settings.USE_GROUNDING,
        timeout_sec=settings.GROUNDING_TIMEOUT_SEC,
        max_attempts=settings.GROUNDING_MAX_ATTEMPTS,
    )

    gen = PPTReportGenerator(service)

    user_data = "이번 달 택시비 120,000원, 커피 65,000원, 배달 180,000원. 절감 제안 포함."
    deck = await gen.generate_ppt_data(user_data)

    print("[AI DEMO] deck result:")
    print(deck)
