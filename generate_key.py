from cryptography.fernet import Fernet
FERNET_KEY = Fernet.generate_key()
key = Fernet.generate_key()
print(key.decode()) 