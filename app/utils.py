from passlib.context import CryptContext


def Hash(password:str):
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
    return pwd_context.hash(password)
