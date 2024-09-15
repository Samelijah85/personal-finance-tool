from ..models.user import User

def userEntity(item) -> User:
    return User(
        username=item["username"],
        email=item["email"],
        full_name=item["full_name"]
    )


def usersEntity(entity) -> list[User]:
    return [userEntity(item) for item in entity]
