from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, PhoneConfirmation


@admin.register(PhoneConfirmation)
class PhoneConfirmationAdmin(admin.ModelAdmin):
    pass


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "phone",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "phone",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("phone",)
    ordering = ("phone",)


admin.site.register(CustomUser, CustomUserAdmin)
