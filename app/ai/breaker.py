import asyncio
from dataclasses import dataclass
from typing import Optional


@dataclass
class CircuitBreaker:
    fail_threshold: int = 5
    reset_timeout_sec: float = 30.0

    _fail_count: int = 0
    _opened_at: Optional[float] = None
    _lock: asyncio.Lock = asyncio.Lock()

    async def allow(self) -> bool:
        async with self._lock:
            if self._opened_at is None:
                return True

            now = asyncio.get_running_loop().time()
            if (now - self._opened_at) >= self.reset_timeout_sec:
                return True
            return False

    async def record_success(self) -> None:
        async with self._lock:
            self._fail_count = 0
            self._opened_at = None

    async def record_failure(self) -> None:
        async with self._lock:
            self._fail_count += 1
            if self._fail_count >= self.fail_threshold and self._opened_at is None:
                self._opened_at = asyncio.get_running_loop().time()