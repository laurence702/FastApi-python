from passlib.context import CryptContext


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashPassword():
    def hash_this(password):
        return  pwd_cxt.hash(password)