from dataclasses import dataclass
from concatenative import inspect, pipe, update


@dataclass
class User:
    id: int
    email: str
    full_name: str


@pipe
def fetch(id: int) -> User:
    # simulate fetching from db
    return User(id=id, email="bademail@example.com", full_name="Example User")


@pipe
def store(user: User) -> int:
    # simulate store into db
    return user.id


def main() -> None:
    f = (
        fetch
        | inspect(lambda u: print(f"fetched: `{u}`"))
        | update(email="user@example.com")
        | inspect(lambda u: print(f"updated: `{u}`"))
        | store
    )
    f(1)


if __name__ == "__main__":
    main()
