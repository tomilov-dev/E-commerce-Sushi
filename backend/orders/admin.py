from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    max_num = 0

    fields = ["unit", "quantity", "price"]
    readonly_fields = ["unit", "quantity", "price"]
    can_delete = False

    verbose_name = "Товарная единица заказа"
    verbose_name_plural = "Товарная единицы заказа"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = [
        "phone",
        "first_name",
        "last_name",
        "address",
        "delivery",
        "payment",
        "client_comment",
        "business_comment",
        "status",
        "order_done",
        "paid_online",
        "paid_online_amount",
    ]

    list_display = [
        "id",
        "status",
        "phone",
        "first_name",
        "last_name",
        "address",
        "order_done",
    ]

    list_editable = ["status", "order_done"]
    list_filter = ["status", "order_done"]

    readonly_fields = [
        "phone",
        "first_name",
        "last_name",
        "address",
        "client_comment",
        "delivery",
        "payment",
        "paid_online",
        "paid_online_amount",
    ]
    inlines = [OrderItemInline]

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if "order_done" in list_display:
            return list_display
        return list_display + ["order_done"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if "order_done__exact" not in request.GET:
            queryset = queryset.filter(order_done=False)
        return queryset
