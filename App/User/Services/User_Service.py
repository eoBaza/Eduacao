from passlib.context import CryptContext

# Hash Senha
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """ Gera o Hash da senha informada """
    return pwd_context.hash(password)

def verifica_password(plain_password: str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def reset_password(password:str, confirmed_password: str) -> bool:
    return password == confirmed_password