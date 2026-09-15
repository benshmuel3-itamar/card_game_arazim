import struct
from os import PathLike

from PIL import Image

from crypt_image import CryptImage


class Card:
    def __init__(
        self, name: str, creator: str, image: CryptImage, riddle: str, solution=None
    ):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self):
        return f"<Card name={self.name},creator={self.creator}"

    def __str__(self):
        ret = f"Card {self.name} by {self.creator}\n"
        ret += f"riddle: {self.riddle}\n"
        sol = self.solution if self.solution is not None else "unsolved"
        ret += f"solution: {sol}"
        return ret

    @classmethod
    def create_from_path(
        cls,
        name: str,
        creator: str,
        riddle: str,
        solution: str,
        path: str | PathLike,
    ):
        image = Image.open(path)
        enc_image = CryptImage(image, key_hash=None)
        return Card(name, creator, enc_image, riddle, solution)

    def serialize(self) -> bytes:
        ret = b""
        name = self.name.encode()
        ret += struct.pack("<I", len(name))
        ret += name
        creator = self.creator.encode()
        ret += struct.pack("<I", len(creator))
        ret += creator
        image = self.image.image
        size = image.size
        bytes = image.tobytes()
        ret += struct.pack("<I", size[0])
        ret += struct.pack("<I", size[1])
        ret += bytes
        ret += self.image.key_hash
        riddle = self.riddle.encode()
        ret += struct.pack("<I", len(riddle))
        ret += riddle
        return ret

    @classmethod
    def deserialize(cls, data: bytes):
        name_length = struct.unpack("<I", data[:4])[0]
        name = data[4 : 4 + name_length].decode()
        data = data[4 + name_length :]
        creator_length = struct.unpack("<I", data[:4])[0]
        creator = data[4 : 4 + creator_length].decode()
        data = data[4 + creator_length :]
        size = (struct.unpack("<I", data[:4])[0], struct.unpack("<I", data[4:8])[0])
        data = data[8:]
        image_bytes = data[: size[0] * size[1] * 3]
        data = data[size[0] * size[1] * 3 :]
        key_hash = data[:32]
        data = data[32:]
        riddle_length = struct.unpack("<I", data[:4])[0]
        riddle = data[4 : 4 + riddle_length].decode()
        data = data[4 + riddle_length :]
        image = CryptImage(
            Image.frombytes(size=size, mode="RGB", data=image_bytes), key_hash
        )
        return Card(name, creator, image, riddle)


name = "coolcards"
creator = "me"
riddle = "whoami"
solution = "itamar12345678901"
path = "image.png"
card = Card.create_from_path(name, creator, riddle, solution, path)
card.image.encrypt(card.solution)
data = card.serialize()
card2 = Card.deserialize(data)
if card2.image.decrypt(solution):
    card2.solution = solution
assert repr(card) == repr(card2)
card2.image.image.show()  # will show the same image as in path
