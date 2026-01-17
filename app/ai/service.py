import asyncio
import logging
from dataclasses import dataclass

from app.ai.breaker import CircuitBreaker
from app.ai.providers import Provider

logger = logging.getLogger("app.ai.service")


def is_transient_error(exc: Exception) -> bool:
    return isinstance(exc, (asyncio.TimeoutError, ConnectionError))


async def sleep_backoff(attempt: int) -> None:
    base = 0.2 * (2 ** attempt)
    jitter = 0.03 * (attempt + 1)
    await asyncio.sleep(min(base + jitter, 2.0))


@dataclass
class AIService:
    grounding: Provider
    basic: Provider
    breaker: CircuitBreaker

    use_grounding: bool = True
    timeout_sec: float = 2.0
    max_attempts: int = 2

    async def get_response(self, prompt: str) -> str:
        if not self.use_grounding:
            return await self.basic.generate(prompt)

        if not await self.breaker.allow():
            logger.warning("grounding_circuit_open -> fast_fallback")
            return await self.basic.generate(prompt)

        for attempt in range(self.max_attempts):
            try:
                result = await asyncio.wait_for(
                    self.grounding.generate(prompt),
                    timeout=self.timeout_sec,
                )
                await self.breaker.record_success()
                return result

            except asyncio.CancelledError:
                raise

            except Exception as e:
                await self.breaker.record_failure()
                logger.warning(
                    "grounding_attempt_failed attempt=%d err=%s",
                    attempt + 1,
                    type(e).__name__,
                )

                if attempt < self.max_attempts - 1 and is_transient_error(e):
                    await sleep_backoff(attempt)
                    continue

                logger.exception("grounding_failed -> fallback")
                return await self.basic.generate(prompt)

        logger.error("unexpected_flow -> fallback")
        return await self.basic.generate(prompt)