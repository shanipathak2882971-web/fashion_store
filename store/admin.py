from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Product,
    CartItem,
    Order,
    OrderItem,
    WishlistItem,
)


# =========================================================
# PRODUCT ADMIN
# =========================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product_image",
        "name",
        "category",
        "price",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "current_image",
    )

    fieldsets = (
        (
            "Product Information",
            {
                "fields": (
                    "name",
                    "category",
                    "price",
                    "description",
                    "current_image",
                    "image",
                )
            },
        ),
    )

    @admin.display(description="Current Image")
    def current_image(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" width="120" height="150" '
                'style="object-fit:cover; border-radius:6px;">',
                obj.image.url
            )

        return "No image uploaded"

    @admin.display(description="Image")
    def product_image(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="object-fit:cover; border-radius:4px;">',
                obj.image.url
            )

        return "No image"


# =========================================================
# CART ITEM ADMIN
# =========================================================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "product",
        "quantity",
        "added_at",
    )

    search_fields = (
        "user__username",
        "product__name",
    )

    ordering = (
        "-added_at",
    )

    readonly_fields = (
        "user",
        "product",
        "quantity",
        "added_at",
    )


# =========================================================
# ORDER ITEM INLINE
# =========================================================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        "product",
        "quantity",
        "price",
    )


# =========================================================
# ORDER ADMIN
# =========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    inlines = [
        OrderItemInline,
    ]

    list_display = (
        "id",
        "user",
        "full_name",
        "email",
        "phone",
        "total_amount",
        "payment_method",
        "status",
        "created_at",
    )

    search_fields = (
        "user__username",
        "full_name",
        "email",
        "phone",
        "city",
        "pin_code",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "user",
                    "full_name",
                    "email",
                    "phone",
                )
            },
        ),
        (
            "Delivery Address",
            {
                "fields": (
                    "address",
                    "city",
                    "pin_code",
                )
            },
        ),
        (
            "Order Information",
            {
                "fields": (
                    "total_amount",
                    "payment_method",
                    "status",
                    "created_at",
                )
            },
        ),
    )


# =========================================================
# ORDER ITEM ADMIN
# =========================================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
    )

    search_fields = (
        "product__name",
        "order__full_name",
        "order__email",
    )


# =========================================================
# WISHLIST ITEM ADMIN
# =========================================================

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "product",
        "added_at",
    )

    search_fields = (
        "user__username",
        "product__name",
    )

    ordering = (
        "-added_at",
    )

    readonly_fields = (
        "user",
        "product",
        "added_at",
    )