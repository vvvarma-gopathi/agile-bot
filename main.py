from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher 
from pwdlib.hashers.bcrypt import BcryptHasher

argon2_hasher=Argon2Hasher(
    time_cost=3,
    memory_cost=6555,
    parallelism=3,
    hash_len=50,
    salt_len=20
)
bcrypt_hasher=BcryptHasher(rounds=12)
password_hash = PasswordHash((argon2_hasher,bcrypt_hasher))
hashed_password = password_hash.hash("varma66")
print(password_hash.verify('varma66',hashed_password))