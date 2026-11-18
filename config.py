"""
Centralized Configuration Module.

Loads environment variables from .env using python-dotenv and exposes
typed constants for browser execution, target URLs, test credentials, and timeouts.
"""
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# URLs
BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com")
API_BASE_URL: str = os.getenv("API_BASE_URL", "https://dummyjson.com")

# Test User Credentials
STANDARD_USER: str = os.getenv("STANDARD_USER", "standard_user")
SECRET_PASSWORD: str = os.getenv("SECRET_PASSWORD", "secret_sauce")
LOCKED_USER: str = os.getenv("LOCKED_USER", "locked_out_user")

# Browser Settings
HEADLESS: bool = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
SLOW_MO: int = int(os.getenv("SLOW_MO", "150"))
DEFAULT_TIMEOUT: float = float(os.getenv("DEFAULT_TIMEOUT", "5000"))
