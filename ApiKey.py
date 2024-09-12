
import os
from cryptography.fernet import Fernet

# 1. 암호화 키 생성 (한 번만 실행)
def generate_key():
    """암호화 키를 생성하고 secret.key 파일에 저장"""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# 2. 암호화 키 로드
def load_key():
    """secret.key 파일에서 암호화 키를 불러옴"""
    if os.path.exists("secret.key"):
        return open("secret.key", "rb").read()
    else:
        print("Error: secret.key 파일이 없습니다.")
        return None

# 3. API 키 암호화
def encrypt_api_key(api_key):
    """API 키를 암호화하고 encrypted_api.key 파일에 저장"""
    key = load_key()
    if key:
        fernet = Fernet(key)
        encrypted_key = fernet.encrypt(api_key.encode())
        with open("encrypted_api.key", "wb") as enc_file:
            enc_file.write(encrypted_key)
        print("API 키가 암호화되었습니다.")
    else:
        print("Error: 암호화 키를 불러오지 못했습니다.")

# 4. API 키 복호화
def decrypt_api_key():
    """encrypted_api.key 파일에서 암호화된 API 키를 복호화"""
    key = load_key()
    if key and os.path.exists("encrypted_api.key"):
        fernet = Fernet(key)
        with open("encrypted_api.key", "rb") as enc_file:
            encrypted_key = enc_file.read()
        return fernet.decrypt(encrypted_key).decode()
    else:
        print("Error: 암호화 키나 encrypted_api.key 파일이 없습니다.")
        return None

# 5. 테스트: 처음에 API 키 암호화 (이미 암호화된 키가 없다면 한 번만 실행)
if not os.path.exists("secret.key"):
    generate_key()
    api_key = ""  # 실제 API 키를 입력하세요
    encrypt_api_key(api_key)

# 6. 프로그램 실행 시 복호화된 API 키 사용
decrypted_api_key = decrypt_api_key()
if decrypted_api_key:
    print(f"복호화된 API 키: {decrypted_api_key}")
else:
    print("API 키를 복호화할 수 없습니다.")
