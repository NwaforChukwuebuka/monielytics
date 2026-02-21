"""Environment-driven configuration."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://username:password@localhost:5432/database_name",
)

# Data path (relative to project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_FILE_PATTERN = "activities_*.csv"

# API
API_PORT = int(os.getenv("PORT", "8080"))
API_HOST = os.getenv("HOST", "0.0.0.0")
