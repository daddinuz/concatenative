from dataclasses import dataclass
from concatenative import *


@dataclass
class User:
    id: int
    email: str
    full_name: str


@wraps
def fetch(id: int) -> User:
    return User(id=id, email="bademail@example.com", full_name="Example User")


@wraps
def store(user: User) -> int:
    return user.id


def update(**kwargs):
    @wraps
    def update(object):
        for key, value in kwargs.items():
            setattr(object, key, value)
        return object
    return update


def project(*args):
    @wraps
    def project(object):
        return {field: getattr(object, field) for field in args}
    return project


def main():
    f = fetch | Then(update(email="user@example.com")) | Inspect(print) | Then(store)
    f(1)


if __name__ == '__main__':
    main()
