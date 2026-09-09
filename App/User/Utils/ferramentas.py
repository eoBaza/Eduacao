# Gerar o Secret Key para API 
import secrets
secret_key = secrets.token_urlsafe(24)
print(secret_key)