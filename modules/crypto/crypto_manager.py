import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class CryptoManager:

    def __init__(self, db_manager, password: str = None, salt: bytes = None):
        self.db_manager = db_manager
        self.backend = default_backend()
        self.master_password = password
        self.salt = salt or os.urandom(16)
        self.key = self._derive_key(password, self.salt)

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = Scrypt(
            salt=salt,
            length=32,  # AES-256 key size
            n=2**14,
            r=8,
            p=1,
            backend=self.backend,
        )
        key = kdf.derive(password.encode())
        return key

    def encrypt(self, data: str) -> bytes:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()

        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted

    def decrypt(self, encrypted_data: bytes, salt: bytes) -> str:
        key = self._derive_key(self.master_password, salt)
        iv = encrypted_data[:16]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        decrypted_padded = decryptor.update(encrypted_data[16:]) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
        return decrypted.decode()

    def get_salt(self) -> bytes:
        return self.salt
