import uuid

from autoslug import AutoSlugField

from dirtyfields import DirtyFieldsMixin

from django.db import models
from django.utils import timezone


class BaseModelWithUID(DirtyFieldsMixin, models.Model):
    class Meta:
        abstract = True

    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class BaseModelWithUidAndSlug(BaseModelWithUID):
    slug = AutoSlugField(populate_from='name', unique=True, always_update=False)
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True
