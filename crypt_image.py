import hashlib
from os import PathLike

from Crypto.Cipher import AES
from PIL import Image


class CryptImage:
    def __init__(self, image: Image, key_hash: bytes):
        self.image = image
        self.key_hash = key_hash

    @classmethod
    def create_from_path(cls, path: str | PathLike):
        return CryptImage(Image.open(path, mode="RGB"), None)

    def _hash(self, val: bytes):
        return hashlib.sha256(hashlib.sha256(val).digest()).digest()

    def encrypt(self, key: str) -> None:
        if self.key_hash != None:
            return
        key = bytes(key, encoding="utf-8")
        self.key_hash = self._hash(key)
        size = self.image.size
        mode = self.image.mode
        plaintext = self.image.tobytes()
        cipher = AES.new(hashlib.sha256(key).digest(), AES.MODE_EAX, nonce=b"arazim")
        encrypted = cipher.encrypt(plaintext)
        self.image = Image.frombytes(size=size, data=encrypted, mode=mode)

    def decrypt(self, key: str) -> bool:
        key = bytes(key, encoding="utf-8")
        if self._hash(key) != self.key_hash:
            return False
        size = self.image.size
        mode = self.image.mode
        plaintext = self.image.tobytes()
        cipher = AES.new(hashlib.sha256(key).digest(), AES.MODE_EAX, nonce=b"arazim")
        encrypted = cipher.decrypt(plaintext)
        self.image = Image.frombytes(size=size, data=encrypted, mode=mode)
        self.key_hash = None
        return True
