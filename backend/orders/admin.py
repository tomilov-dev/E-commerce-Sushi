from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["unit"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "status",
        "phone",
        "first_name",
        "last_name",
        "address",
    ]

    list_editable = ["status"]
    list_filter = ["status"]

    readonly_fields = [
        "phone",
        "first_name",
        "last_name",
        "address",
        "client_comment",
    ]
    inlines = [OrderItemInline]
