"""
- 해당 레포의 entryponint
- 비동기/보안/AI/환경분리를 데모로 실행함

포인트
1) argparse로 실행 모드를 분기하는 패턴
2) asyncio.run()으로 비동기 main 루프를 구동
3) Settings / Logging를 앱 시작 시점에 초기화하는 패턴

- Settings.from_env()로 환경변수를 로드
- setup_logging()으로 로깅을 설정
-> 둘다 .env 파일이 없으면 에러남, "맨 앞"에서 1번만 실행되도록 함
- 이후 모듈들에서 logging.getLogger()로 logger를 쓰면, 앱 정책이 전체적으로 일관되게 적용 됨.
"""


import argparse # 명령줄 인자(플래그)를 파싱하기 위한 표준 라이브러리
import asyncio # 비동기 프로그래밍 라이브러리

# 모듈 임포트 (설정, 로깅, 각 데모 함수 등)
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
    """
    CLI 인자 파싱
    -- demo 옵션으로 특정 데모만 실행하거나, 전부 실행할 수 있다.

    - 실제 서비스에서도 "admin 명령어"를 이런 식으로 분리해두면 유용할지도?
    - "모든 데모 실행"은 실제로는 잘 안 쓰겠지만, 테스트/CI 등에서는 편함.
    - ex) python main.py --task warm_cashe, python main.py --task migrate_db

    """

async def main():
    """비동기 메인 함수"""
    args = parse_args() # 사용자가 입력한 인자 값을 가져온다.
    settings = Settings.from_env() # 환경변수에서 설정 로드 -> 객체 생성
    setup_logging(settings.LOG_LEVEL) # 설정된 레벨로 로깅 초기화

    # 선택한 모드에 따라 해당 비동기 데모 함수를 실행한다 (await는 필수!!)
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