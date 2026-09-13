from .models import CartItem, WishlistItem


def cart_wishlist_counts(request):

    if request.user.is_authenticated:
        cart_count = sum(
            item.quantity
            for item in CartItem.objects.filter(user=request.user)
        )

        wishlist_count = WishlistItem.objects.filter(
            user=request.user
        ).count()

    else:
        cart_count = 0
        wishlist_count = 0

    return {
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
    }