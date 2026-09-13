import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Any

from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api.models import User


password_hasher = PasswordHash.recommended()


def load_users(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as file:
        data: Any = json.load(file)

    if not isinstance(data, list):
        raise ValueError("The users file must contain a JSON list")

    users: list[dict[str, str]] = []
    usernames: set[str] = set()

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"User at index {index} must be an object")

        username = item.get("username")
        password = item.get("password")

        if not isinstance(username, str) or not username.strip():
            raise ValueError(f"User at index {index} has an invalid username")

        if not isinstance(password, str) or not password:
            raise ValueError(f"User at index {index} has an invalid password")

        username = username.strip()

        if username in usernames:
            raise ValueError(f"Duplicate username in input file: {username}")

        usernames.add(username)
        users.append(
            {
                "username": username,
                "password": password,
            }
        )

    return users


async def add_users(database_url: str, users_file: Path) -> None:
    users = load_users(users_file)

    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    created = 0
    skipped = 0

    try:
        async with session_factory.begin() as session:
            for user_data in users:
                result = await session.execute(
                    select(User).where(
                        User.username == user_data["username"]
                    )
                )

                existing_user = result.scalar_one_or_none()

                if existing_user is not None:
                    print(
                        f"Skipping existing user: "
                        f"{user_data['username']}"
                    )
                    skipped += 1
                    continue

                user = User(
                    username=user_data["username"],
                    hashed_password=password_hasher.hash(
                        user_data["password"]
                    ),
                )

                session.add(user)
                created += 1

        print(f"Created: {created}, skipped: {skipped}")

    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add users to the application database"
    )

    parser.add_argument(
        "--database-url",
        default=os.environ.get("DATABASE_URL"),
        help=(
            "SQLAlchemy database URL. "
            "Can also be provided through DATABASE_URL."
        ),
    )

    parser.add_argument(
        "--users-file",
        type=Path,
        required=True,
        help="Path to the JSON file containing users",
    )

    args = parser.parse_args()

    if not args.database_url:
        parser.error(
            "Provide --database-url or set the DATABASE_URL environment variable"
        )

    asyncio.run(add_users(args.database_url, args.users_file))


if __name__ == "__main__":
    main()
