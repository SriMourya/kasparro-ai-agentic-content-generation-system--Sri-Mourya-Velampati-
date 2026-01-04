import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    # Add other settings as needed
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MIN_FAQ_COUNT: int = 15

    def validate(self):
        if not self.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")

settings = Settings()
