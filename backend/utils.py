import os
import uuid
import hashlib


def image_filename(instance, filename) -> None:
    ext = filename.split(".")[-1]
    hash_part = hashlib.md5(instance.name.encode("utf-8")).hexdigest()
    uuid_part = str(uuid.uuid4())

    filename = f"{hash_part}-{uuid_part}.{ext}"
    return os.path.join("images/", filename)
