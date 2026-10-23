import base64
import hashlib
import hmac
import secrets


ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 310_000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS
    )
    salt_text = base64.urlsafe_b64encode(salt).decode("ascii").rstrip("=")
    digest_text = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return f"{ALGORITHM}${ITERATIONS}${salt_text}${digest_text}"


def verify_password(password: str, stored_password: str) -> tuple[bool, bool]:
    if not stored_password.startswith(f"{ALGORITHM}$"):
        return hmac.compare_digest(password, stored_password), True

    try:
        algorithm, iterations_text, salt_text, digest_text = stored_password.split("$")
        if algorithm != ALGORITHM:
            return False, False

        iterations = int(iterations_text)
        salt = base64.urlsafe_b64decode(salt_text + "=" * (-len(salt_text) % 4))
        expected = base64.urlsafe_b64decode(
            digest_text + "=" * (-len(digest_text) % 4)
        )
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, iterations
        )
    except (TypeError, ValueError):
        return False, False

    return hmac.compare_digest(actual, expected), False