from decimal import Decimal

from autoslug import AutoSlugField

from django.db import models
from django.contrib.auth import get_user_model

from simple_history.models import HistoricalRecords

from shared.models import BaseModelWithUID

from .choices import *

User = get_user_model()


class Order(BaseModelWithUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    restaurant = models.ForeignKey(
        "restaurant.Restaurant", on_delete=models.CASCADE, related_name="orders"
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    delivery_status = models.CharField(
        max_length=50,
        choices=DeliveryStatusChoices.choices,
        db_index=True,
        default=DeliveryStatusChoices.PENDING,
    )
    order_status = models.CharField(
        max_length=50,
        choices=OrderStatusChoices.choices,
        db_index=True,
        default=OrderStatusChoices.PENDING,
    )
    order_type = models.CharField(
        max_length=50,
        choices=OrderTypeChoices.choices,
        db_index=True,
        default=OrderTypeChoices.DELIVERY,
    )
    delivery_man = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    delivery_address = models.CharField(max_length=255)

    # simple history
    history = HistoricalRecords()

    def __str__(self):
        return (
            f"Restaurant Order {self.restaurant.name} for user {self.user.get_name()}"
        )


class OrderItem(BaseModelWithUID):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    menu_item = models.OneToOneField("restaurant.MenuItem", on_delete=models.CASCADE)
    modifier = models.ForeignKey(
        "restaurant.Modifier",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"


class Cart(BaseModelWithUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.get_name()} , uid - {self.user.uid}"


class CartItem(BaseModelWithUID):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    menu_item = models.OneToOneField("restaurant.MenuItem", on_delete=models.CASCADE)
    modifier = models.ForeignKey(
        "restaurant.Modifier",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"


class Payment(BaseModelWithUID):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=50, choices=PaymentMethodChoices.choices
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PaymentStatusChoices.choices,
        db_index=True,
        default=PaymentStatusChoices.PENDING,
    )

    # simple history
    history = HistoricalRecords()

    def __str__(self):
        return f"Payment for order uid - {self.order.uid}"


# Model for storing the feedback of customers on various aspects
class CustomerFeedback(BaseModelWithUID):
    slug = AutoSlugField(populate_from="title", unique=True, always_update=False)
    title = models.CharField(max_length=30)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="feedbacks"
    )
    menu_item = models.ForeignKey(
        "restaurant.MenuItem",
        on_delete=models.CASCADE,
        related_name="feedbacks",
        null=True,
        blank=True,
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="feedbacks", null=True, blank=True
    )
    restaurant = models.ForeignKey(
        "restaurant.Restaurant",
        on_delete=models.CASCADE,
        related_name="feedbacks",
        null=True,
        blank=True,
    )
    rating = models.PositiveIntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Feedback from {self.user.get_name()} on {self.menu_item.name}"
