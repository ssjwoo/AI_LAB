import os
from dataclasses import dataclass


def _to_bool(v: str, default: bool = False) -> bool:
    """ 문자열 환경변수(true, 1, yes)-> bool로 변환하는 함수"""
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "t", "yes", "y", "on")


@dataclass(frozen=True) # 객체 생성 후 수정 불가(불변) -> 실수로 값을 바꾸는 것을 방지
class Settings:
    """환경변수를 모아놓은 설정 객체"""
    DEV_MODE: bool # 개발 모드 여부
    LOG_LEVEL: str # 로깅 레벨

    USE_GROUNDING: bool # 외부 검색/DB 연동 사용 여부
    GROUNDING_TIMEOUT_SEC: float # 외부 호출 타임아웃
    GROUNDING_MAX_ATTEMPTS: int # 외부 호출 최대 재시도 횟수

    CB_FAIL_THRESHOLD: int # 서킷브레이커 실패 임계치
    CB_RESET_TIMEOUT_SEC: float # 서킷브레이커 리셋 대기 시간

    HIDE_EXISTENCE_ON_UNAUTHORIZED: bool # 권한 없음 에러 시, 404로 처리(존재 은닉) 여부

    @classmethod
    def from_env(cls) -> "Settings":
        """환경변수에서 설정 객체 생성"""
        return cls(
            DEV_MODE=_to_bool(os.getenv("DEV_MODE"), default=True),
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO").upper(),

            USE_GROUNDING=_to_bool(os.getenv("USE_GROUNDING"), default=True),
            GROUNDING_TIMEOUT_SEC=float(os.getenv("GROUNDING_TIMEOUT_SEC", "2.0")),
            GROUNDING_MAX_ATTEMPTS=int(os.getenv("GROUNDING_MAX_ATTEMPTS", "2")),

            CB_FAIL_THRESHOLD=int(os.getenv("CB_FAIL_THRESHOLD", "5")),
            CB_RESET_TIMEOUT_SEC=float(os.getenv("CB_RESET_TIMEOUT_SEC", "30.0")),

            HIDE_EXISTENCE_ON_UNAUTHORIZED=_to_bool(
                os.getenv("HIDE_EXISTENCE_ON_UNAUTHORIZED"), default=False
            ),
        )