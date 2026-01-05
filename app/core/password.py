import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with automatic salting.

    bcrypt internally:
    - generates a random salt
    - embeds salt + cost inside the hash
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)  # production-safe cost
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against the stored bcrypt hash.
    """
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
