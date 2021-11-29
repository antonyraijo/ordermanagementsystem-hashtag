from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):

    model = get_user_model()
    list_display = ("id", "name", "email", "is_consumer", "is_superuser", "is_staff", "is_active", "date_joined")
    list_filter = ("is_consumer", "is_superuser", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("name", "email", "date_joined", "password")}),
        ("Permissions", {"fields": ("is_consumer", "is_superuser", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "email",
                    "is_consumer",
                    "date_joined",
                    "password1",
                    "password2",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.site_header = "Order Management"
admin.site.site_title = "Order Management Portal"
admin.site.index_title = "Welcome To Order Management Portal"