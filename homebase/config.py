from __future__ import annotations
from pydantic import BaseModel, Field
from pathlib import Path
import os

class HomebaseConfig(BaseModel):
    """
    Central configuration object for Homebase.
    Loaded from environment variables (.env file).
    """
    vault_path: Path = Field(..., description="Path to your Obsidian vault")
    timezone: str = Field("America/Chicago", description="IANA timezone name")
    output_daily_dir: str = Field("Assignments/Daily", description="Subfolder for daily notes")
    output_master_file: str = Field("Assignments/Master.md", description="File for master log")

def load_config() -> HomebaseConfig:
    """
    Loads configuration from environment variables.
    Requires python-dotenv to pre-load .env file into os.environ.
    """
    from dotenv import load_dotenv
    load_dotenv()  # will silently do nothing if no .env file exists

    vault = os.getenv("HOMEBASE_VAULT_PATH")
    tz = os.getenv("HOMEBASE_TZ", "America/Chicago")
    daily_dir = os.getenv("HOMEBASE_DAILY_DIR", "Assignments/Daily")
    master_file = os.getenv("HOMEBASE_MASTER_FILE", "Assignments/Master.md")

    if not vault:
        raise RuntimeError("HOMEBASE_VAULT_PATH is not set. Run `homebase init` to create a .env file.")

    return HomebaseConfig(
        vault_path=Path(vault).expanduser().resolve(),
        timezone=tz,
        output_daily_dir=daily_dir,
        output_master_file=master_file,
    )
