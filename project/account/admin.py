from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ["uid", "first_name", "last_name", "phone", "email", "image", "status"]
    list_filter = ["is_superuser", "is_staff", "status"]
    search_fields = ("phone", "first_name", "last_name")
    readonly_fields = ("password", "uid", "slug")
    ordering = ("-created_at",)

