from passlib.context import CryptContext

# Hash Senha
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """ Gera o Hash da senha informada """
    return pwd_context.hash(password)

def verifica_password(plain_password: str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



# ====== TESTE de senha 
senha_user = 'Ph25060707'
senha_digitada='Ph25060707'
senha_cript = hash_password(senha_user)
print(f"senha criptografada {senha_cript}")

if verifica_password(senha_digitada, senha_cript):
    print("login correto")
else:
    print("erro na senha")