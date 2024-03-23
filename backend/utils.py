import os
import uuid
import hashlib
from slugify import slugify
from django.db import models


def image_filename(
    instance: models.Model,
    filename: str,
    extension: str | None = None,
) -> str:
    if not extension:
        extension = filename.split(".")[-1]

    hash_part = hashlib.md5(instance.name.encode("utf-8")).hexdigest()
    uuid_part = str(uuid.uuid4())

    filename = f"{hash_part}-{uuid_part}.{extension}"
    return os.path.join("images/", filename)


def get_slug(
    orm: models.Model,
    name: str,
) -> str:
    original_slug = slugify(name)
    slug = original_slug

    counter = 1
    while orm.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{counter}"

    return slug
