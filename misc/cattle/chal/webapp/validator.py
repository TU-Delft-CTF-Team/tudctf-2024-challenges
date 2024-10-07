import io
import json

from imagehash import ImageHash, average_hash, hex_to_hash
from PIL import Image


class Validator:
    def __init__(self, hash_file: str, threshold: int = 3):
        self.threshold = threshold

        with open(hash_file) as f:
            data: dict[str, str] = json.load(f)

        self.hash_data: list[ImageHash] = [
            hex_to_hash(entry) for entry in data.values()
        ]

    def validate(self, image_data: bytes) -> bool:
        try:
            image = Image.open(io.BytesIO(image_data))

            avg_hash_val = average_hash(image)

            for entry in self.hash_data:
                if abs(entry - avg_hash_val) <= self.threshold:
                    return True
        except Exception:
            pass

        return False
