import uuid

from django.db import models


class Token(models.Model):
    """Маркер"""
    email = models.EmailField()
    uid = models.CharField(
        max_length=40,
        default=uuid.uuid4,
    )
