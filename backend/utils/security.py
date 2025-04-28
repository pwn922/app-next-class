from werkzeug.security import generate_password_hash, check_password_hash


def generate_secure_password(password):
    hashed_password = generate_password_hash(password)
    return hashed_password


def verify_password(hashed_password, plain_password):
    return check_password_hash(hashed_password, plain_password)
