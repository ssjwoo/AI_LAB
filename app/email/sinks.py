import hashlib
import logging
from abc import ABC, abstractmethod
from pathlib import Path

import aiofiles

logger = logging.getLogger("app.email")


class EmailSink(ABC):
    @abstractmethod
    async def send(self, to_addr: str, content: str) -> None:
        raise NotImplementedError


class LocalFileSink(EmailSink):
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True, parents=True)

    async def send(self, to_addr: str, content: str) -> None:
        safe = hashlib.sha256(to_addr.encode("utf-8")).hexdigest()[:12]
        file_path = self.output_dir / f"{safe}.html"

        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(content)

        logger.info("email_saved_locally path=%s user_hash=%s", str(file_path), safe)


class SmtpSink(EmailSink):
    async def send(self, to_addr: str, content: str) -> None:
        safe = hashlib.sha256(to_addr.encode("utf-8")).hexdigest()[:12]
        logger.info("email_sent_via_smtp user_hash=%s content_bytes=%d", safe, len(content.encode("utf-8")))