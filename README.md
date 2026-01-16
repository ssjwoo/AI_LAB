# admin_lab

`admin_lab`는 개인 학습/복습을 위해 만든 **범용 백엔드 설계 패턴 실습용 mini-lab**입니다.  
외부 의존(검색/AI), 환경 분리(DEV/PROD), 출력 형식 통제, 인가/보안, 비동기 동시성 같은 주제를 **작게 쪼개어 직접 실행해 보며 체감**하는 것을 목표로 합니다.

이 레포는 특정 서비스(도메인)에 종속되지 않도록 구성되어 있어, 비슷한 문제를 다른 프로젝트에도 그대로 적용할 수 있습니다.

---

## What this repo demonstrates

### 1) 환경 분리 및 관측성 (Environment Switch + Observability)
- `DEV_MODE` 환경변수에 따라 이메일 발송을 **Sink(인터페이스) 주입**으로 분기
  - DEV: HTML 파일로 저장 (`LocalFileSink`, `aiofiles` 사용)
  - PROD: SMTP/API 자리 (`SmtpSink`, 데모에서는 로그만)
- PII 보호를 위해 이메일 원문을 파일명/로그에 남기지 않고 **해시 기반 식별자** 사용
- 로깅을 통해 “어떤 이벤트가 어떤 맥락에서 발생했는지” 추적 가능

### 2) 외부 의존 실패에 강한 설계 (Timeout/Retry/Circuit Breaker/Fallback)
외부 API(검색/grounding 등)는 실패할 수 있다는 전제로,
- **Timeout**: 무한 대기 방지
- **Retry**: transient error(타임아웃/커넥션 오류)만 제한적으로 재시도
- **Circuit Breaker**: 장애 지속 시 fast-fail로 즉시 우회
- **Fallback**: 실패해도 기능이 멈추지 않도록 기본 로직으로 우회
를 통해 안정적으로 동작하도록 구성합니다.

### 3) AI 출력 형식 통제 (Prompt + Schema Validation + Repair)
프롬프트만으로 100% 형식 준수는 어렵기 때문에,
- Pydantic 스키마(`Deck`, `Slide`)로 **구조 검증**
- 파싱 실패 시 **Repair 1회 재요청**
- 그래도 실패하면 **기본 템플릿 Fallback**
을 통해 “불확실한 출력”을 코드로 제어합니다.

### 4) 인가/보안 기초 (RBAC + Ownership)
인증(Authentication) 이후에도 인가(Authorization)가 빠지면 리소스 탈취(IDOR 등)가 발생할 수 있습니다.
- 리소스 존재 여부(404)와 권한 없음(403)을 분리
- 필요 시 존재 은닉 전략: `HIDE_EXISTENCE_ON_UNAUTHORIZED=true`면 권한 없음도 404로 통일 가능
- Admin role 예외 처리 및 ownership 검증을 정책 레이어로 강제

### 5) 비동기 동시성 제어 (Semaphore)
무제한 `gather()`는 시스템 리소스(특히 DB 커넥션 풀)를 고갈시킬 수 있으므로,
- `asyncio.Semaphore`로 동시 실행 개수를 제한
- 순차 처리 대비 병렬 처리(제한 적용)의 시간 차이를 수치로 확인

---

## Repo structure
admin_ai_lab/
main.py
requirements.txt
app/
core/ # settings, logging
email/ # sink interface + dev/prod impl
ai/ # provider, breaker, timeout/retry/fallback
security/ # RBAC + ownership authorization
demos/ # runnable demos


---

## Requirements
- Python 3.10+ (WSL Ubuntu 기준)
- Dependencies: `pydantic`, `aiofiles`

---

## Install & Run

### 1) Create venv and install deps
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### 2) Run all demos
python main.py

### 3) Run a specific demo
python main.py --demo ai
python main.py --demo email
python main.py --demo security
python main.py --demo async

### Environment variables
DEV/PROD switch

DEV_MODE=true|false

true: 이메일을 로컬 파일로 저장 (./mock_emails/)

false: SMTP sink 사용(데모에서는 로그만)

export DEV_MODE=true
python main.py --demo email
ls -la mock_emails

AI / Resilience policies

USE_GROUNDING=true|false

GROUNDING_TIMEOUT_SEC=2.0

GROUNDING_MAX_ATTEMPTS=2

CB_FAIL_THRESHOLD=5

CB_RESET_TIMEOUT_SEC=30

export USE_GROUNDING=true
export GROUNDING_TIMEOUT_SEC=1.0
export GROUNDING_MAX_ATTEMPTS=2
export CB_FAIL_THRESHOLD=2
export CB_RESET_TIMEOUT_SEC=10
python main.py --demo ai

Authorization policy

HIDE_EXISTENCE_ON_UNAUTHORIZED=true|false

true: 권한 없을 때도 404(존재 은닉)

false: 권한 없을 때 403

export HIDE_EXISTENCE_ON_UNAUTHORIZED=true
python main.py --demo security

How to practice (suggested)

DEV_MODE를 바꿔가며 sink 전환을 체감하고, 파일이 생성되는지 확인

CB_FAIL_THRESHOLD, CB_RESET_TIMEOUT_SEC를 바꿔가며 breaker가 언제 열리고 닫히는지 로그로 확인

USE_GROUNDING=false로 두고도 기능이 정상 동작하는지 확인(우회 경로 검증)

HIDE_EXISTENCE_ON_UNAUTHORIZED를 켜고/끄며 403/404 정책 차이를 체감

async 데모에서 n, limit을 바꿔가며 “동시성 제한이 왜 필요한지” 시간으로 확인

Notes / Next improvements (optional)

실제 SMTP 연동, HTTP client 기반 외부 호출(httpx) 추가

JSON 구조화 로깅(예: structlog) 적용

pytest로 권한/파싱/서킷브레이커 동작 테스트 자동화

스케일 환경에서 breaker/limit 상태 공유를 위한 Redis 도입
