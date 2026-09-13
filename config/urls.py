from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from store.views import login_view, my_orders
from store.views import (
    home,
    shop,
    product_detail,
    add_to_cart,
    buy_now,
    cart,
    remove_from_cart,
    update_cart_quantity,
    checkout,
    order_success,
    wishlist,
    add_to_wishlist,
    remove_from_wishlist,
    wishlist_add_to_cart,
    login_view,
    signup_view,
    logout_view,
    account_view,   
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("account/", account_view, name="account"),
    path("orders/", my_orders, name="my_orders"),
    path("", home, name="home"),
    path("shop/", shop, name="shop"),
    path("product/<int:product_id>/", product_detail, name="product_detail"),
    path("product/<int:product_id>/add-to-cart/", add_to_cart, name="add_to_cart"),
    path("product/<int:product_id>/buy-now/", buy_now, name="buy_now"),
    path("cart/", cart, name="cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path(
         "cart/update/<int:item_id>/<str:action>/",
          update_cart_quantity,
          name="update_cart_quantity"),

    path("checkout/", checkout, name="checkout"),
    path("order-success/", order_success, name="order_success"),
    path("wishlist/", wishlist, name="wishlist"),
    path(
         "product/<int:product_id>/add-to-wishlist/",
          add_to_wishlist,
          name="add_to_wishlist"
        ),
    path(
         "wishlist/remove/<int:item_id>/",
          remove_from_wishlist,
          name="remove_from_wishlist"
        ),
    path(
         "wishlist/add-to-cart/<int:item_id>/",
          wishlist_add_to_cart,
          name="wishlist_add_to_cart"
        ),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )