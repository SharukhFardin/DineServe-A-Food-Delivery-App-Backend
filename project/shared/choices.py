from django.db import models


class StatusChoices(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    REMOVED = "REMOVED", "Removed"


class StaffRoleChoices(models.TextChoices):
    OWNER = "OWNER", "Owner"
    MANAGER = "MANAGER", "Manager"
    CHEF = "CHEF", "Chef"
    WAITER = "WAITER", "Waiter"
    CASHIER = "CASHIER", "Cashier"
    DELIVERY = "DELIVERY", "Delivery Staff"
    ASSISTANT = "ASSISTANT", "Assistant"
    EMPLOYEE = "EMPLOYEE", "Employee" # Default role
