from pathlib import Path

from app.core.settings import Settings
from app.email.sinks import LocalFileSink, SmtpSink


async def demo_email(settings: Settings):
    sink = LocalFileSink(Path("./mock_emails")) if settings.DEV_MODE else SmtpSink()
    content = "<html><body><h1>Weekly Report</h1><p>Hello</p></body></html>"
    await sink.send("user@example.com", content)
    print(f"[EMAIL DEMO] DEV_MODE={settings.DEV_MODE} -> done")
