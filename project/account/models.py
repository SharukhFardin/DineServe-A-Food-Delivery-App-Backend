"""Models related to User Accounts will be stored here"""

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from autoslug import AutoSlugField

from phonenumber_field.modelfields import PhoneNumberField

from simple_history.models import HistoricalRecords

from shared.models import BaseModelWithUID

from .choices import UserStatus
from .managers import CustomUserManager
from .utils import get_slug_full_name


class User(AbstractBaseUser, PermissionsMixin, BaseModelWithUID):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from=get_slug_full_name, editable=False, unique=True)
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(unique=True, db_index=True)
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        db_index=True,
        default=UserStatus.ACTIVE,
    )
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")

    # Managers
    objects = CustomUserManager()

    # simple history
    history = HistoricalRecords()

    def __str__(self):
        name = " ".join([self.first_name, self.last_name])
        return (
            f"Name: {name}, Email: {self.email}"
            if len(self.email) > 0
            else f"Name: {name} Phone: {self.phone}"
        )

    def get_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        name = f"{self.first_name} {self.last_name}"
        return name.strip()

    def activate(self):
        self.status = UserStatus.ACTIVE
        self.save_dirty_fields()

    def deactivate(self):
        self.status = UserStatus.INACTIVE
        self.save_dirty_fields()

    def removed(self):
        self.status = UserStatus.REMOVED
        self.is_active = False
        self.save_dirty_fields()
