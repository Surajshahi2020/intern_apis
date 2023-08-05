from django.db import models
from uuid import uuid4


class CommonInfo(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    created_at = models.DateTimeField("Created at", auto_now_add=True, db_index=True)
    creator = models.ForeignKey(
        "internapp.User",
        verbose_name="Created by",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_creator",
        on_delete=models.SET_NULL,
    )
    modified_at = models.DateTimeField("Last modified at", auto_now=True, db_index=True)
    modifier = models.ForeignKey(
        "internapp.User",
        verbose_name="Modified_by",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_modifier",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
