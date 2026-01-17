import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """ 애플리케이션 전체의 로깅 설정을 초기화하는 함수 """
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
    )