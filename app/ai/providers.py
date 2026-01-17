from typing import Protocol


class Provider(Protocol):
    async def generate(self, prompt: str) -> str: ...


class GroundingProvider:
    async def generate(self, prompt: str) -> str:
        return f'{{"slides":[{{"title":"Grounding","content":"{prompt} 실시간 기반 요약"}}]}}'


class FlakyGroundingProvider:
    def __init__(self, fail_every: int = 2):
        self.fail_every = max(1, fail_every)
        self._count = 0

    async def generate(self, prompt: str) -> str:
        self._count += 1
        if self._count % self.fail_every == 0:
            raise ConnectionError("Simulated grounding outage")
        return f'{{"slides":[{{"title":"Grounding OK","content":"{prompt} (ok)"}}]}}'


class BasicProvider:
    async def generate(self, prompt: str) -> str:
        return f'{{"slides":[{{"title":"Basic","content":"{prompt} 일반 요약"}}]}}'