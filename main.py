import argparse
import asyncio

from app.core.logging import setup_logging
from app.core.settings import Settings

from app.demos.async_demo import demo_async
from app.demos.security_demo import demo_security
from app.demos.ai_demo import demo_ai
from app.demos.email_demo import demo_email


def parse_args():
    p = argparse.ArgumentParser(description="Run demo scripts")
    p.add_argument("--demo", type=str, choices=["async", "security", "ai", "email"], default="async")
    return p.parse_args()

async def main():
    args = parse_args()
    settings = Settings.from_env()
    setup_logging(settings.LOG_LEVEL)

    if args.demo in ("ai", "all"):
        await demo_ai(settings)
    if args.demo in ("email", "all"):
        await demo_email(settings)
    if args.demo in ("security", "all"):
        await demo_security(settings)
    if args.demo in ("async", "all"):
        await demo_async()


if __name__ == "__main__":
    asyncio.run(main())