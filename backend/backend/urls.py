from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

admin.site.site_title = "Админ-панель"
admin.site.site_header = "Админ-панель сайта доставки"
admin.site.index_title = "Администрирование"

urlpatterns = [
    path("", include("pages.urls", namespace="pages")),
    path("admin/", admin.site.urls),
    path("products/", include("products.urls", namespace="products")),
    path("categories/", include("categories.urls", namespace="categories")),
    path("promo/", include("promotion.urls", namespace="promotion")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("account/", include("accounts.urls", namespace="accounts")),
    path("payment/", include("online_payment.urls", namespace="payment")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     import debug_toolbar

#     urlpatterns += [
#         path("__debug__/", include(debug_toolbar.urls)),
#     ]
