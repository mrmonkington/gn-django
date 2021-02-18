from django.db import models


class UpdatableModel(models.Model):
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
