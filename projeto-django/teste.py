import secrets

secret_key = secrets.token_bytes(32)
print(secret_key.hex())
