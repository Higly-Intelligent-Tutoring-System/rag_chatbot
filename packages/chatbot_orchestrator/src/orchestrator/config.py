import os
from dotenv import load_dotenv

load_dotenv()

SAVER_BACKEND: str = os.getenv("SAVER_BACKEND", "memory")
SERVER_BACKEND: str = os.getenv("SERVER_BACKEND", "memory")

POSTGRES_USERNAME: str = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DOMAIN: str = os.getenv("POSTGRES_DOMAIN", "localhost")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5442")
POSTGRES_SSL: str = os.getenv("POSTGRES_SSL", "false")

DB_URI=f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_DOMAIN}:{POSTGRES_PORT}/postgres?sslmode={POSTGRES_SSL}"