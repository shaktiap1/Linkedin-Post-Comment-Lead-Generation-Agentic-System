from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):

    linkedin_email: str
    linkedin_password: str

    google_service_account_file: str
    google_sheet_name: str

    max_concurrent_tasks: int = 3
    scraper_retry_limit: int = 3

    scroll_pause_seconds: int = 2
    request_delay_min: int = 1
    request_delay_max: int = 3


def load_settings():

    return Settings(
        linkedin_email=os.getenv("LINKEDIN_EMAIL"),
        linkedin_password=os.getenv("LINKEDIN_PASSWORD"),
        google_service_account_file=os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE"),
        google_sheet_name=os.getenv("GOOGLE_SHEET_NAME"),
        max_concurrent_tasks=int(os.getenv("MAX_CONCURRENT_TASKS", 3)),
        scraper_retry_limit=int(os.getenv("SCRAPER_RETRY_LIMIT", 3)),
        scroll_pause_seconds=int(os.getenv("SCROLL_PAUSE_SECONDS", 2)),
        request_delay_min=int(os.getenv("REQUEST_DELAY_MIN", 1)),
        request_delay_max=int(os.getenv("REQUEST_DELAY_MAX", 3)),
    )


settings = load_settings()