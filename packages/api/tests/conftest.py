import sys
import pytest
from pathlib import Path
from dotenv import load_dotenv

repo_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(repo_root / "packages" / "api" / "src"))

load_dotenv(repo_root / "envs/.env.dev.ita")