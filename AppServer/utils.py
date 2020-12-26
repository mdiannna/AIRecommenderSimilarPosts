import hashlib

def create_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def check_password(real_password_hash, tested_password):
    hashed_test = create_hash(tested_password)

    if real_password_hash == hashed_test:
        return True

    return False
