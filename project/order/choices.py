from django.db import models


class DeliveryStatusChoices(models.TextChoices):
    PENDING = "PENDING", "Pending"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for Delivery"
    DELIVERED = "DELIVERED", "Delivered"
    CANCELLED = "CANCELLED", "Cancelled"


class PaymentMethodChoices(models.TextChoices):
    CARD = "CARD", "Card"
    CASH = "CASH", "Cash"
    PAYPAL = "PAYPAL", "Paypal"
    BKASH = "BKASH", "Bkash"
    # more options can be implemented in future


class PaymentStatusChoices(models.TextChoices):
    PENDING = "PENDING", "Pending"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"


class OrderStatusChoices(models.TextChoices):
    PENDING = "PENDING", "Pending"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"


class OrderTypeChoices(models.TextChoices):
    DELIVERY = "DELIVERY", "Delivery"
    TAKEAWAY = "TAKEAWAY", "Takeaway"
