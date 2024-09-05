from django.db import models

from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

from simple_history.models import HistoricalRecords

from shared.models import BaseModelWithUID ,BaseModelWithUidAndSlug
from shared.choices import StatusChoices, StaffRoleChoices

User = get_user_model()


class Restaurant(BaseModelWithUidAndSlug):
    CEO_name = models.CharField(max_length=30)
    tax_number = models.CharField(max_length=50, unique=True)
    registration_no = models.CharField(max_length=50, unique=True)
    contact_number = PhoneNumberField(blank=True, null=True)
    website_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    whatsapp_no = PhoneNumberField(blank=True, null=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        db_index=True,
        default=StatusChoices.ACTIVE,
    )
    number_of_employees = models.PositiveIntegerField(null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    delivery = models.BooleanField(default=False)
    takeaway = models.BooleanField(default=False)

    # simple history
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def get_restaurant_staffs(self):
        return self.organizationuser_set.filter(role=StaffRoleChoices.EMPLOYEE)

    def activate(self):
        self.status = StatusChoices.ACTIVE
        self.save_dirty_fields()

    def deactivate(self):
        self.status = StatusChoices.INACTIVE
        self.save_dirty_fields()


class RestaurantStaff(models.Model):
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        db_index=True,
        default=StatusChoices.ACTIVE,
    )
    # is_default field will come in handy if a staff works in multiple restaurants
    is_default = models.BooleanField(default=False)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=StaffRoleChoices.choices,
        db_index=True,
        default=StaffRoleChoices.EMPLOYEE,
    )

    # simple history
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.get_name()} - {self.role} at {self.restaurant.name}"


class RestaurantAddress(BaseModelWithUID):
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    street = models.CharField(max_length=255, null=True, blank=True)
    road = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    country = models.CharField(max_length=100)

    # simple history
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"


class MenuCategory(BaseModelWithUidAndSlug):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_categories')

    # simple history
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    

class MenuItem(BaseModelWithUidAndSlug):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    menu_category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='menu_items')
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)

    # simple history
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    

class Modifier(BaseModelWithUidAndSlug):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='modifiers')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='modifiers/', null=True, blank=True)

    # simple history
    history = HistoricalRecords()

    def __str__(self):
        return self.name