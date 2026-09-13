from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import (
    Product,
    CartItem,
    Order,
    OrderItem,
    WishlistItem,
)


# =========================================================
# HOME
# =========================================================

def home(request):
    products = Product.objects.all().order_by("-created_at")

    return render(
        request,
        "store/home.html",
        {
            "products": products
        }
    )


# =========================================================
# SHOP
# =========================================================

def shop(request):

    products = Product.objects.all()

    search = request.GET.get("search", "").strip()
    sort = request.GET.get("sort", "")
    category = request.GET.get("category", "").strip()

    if search:
        products = products.filter(
            name__icontains=search
        )

    if category:
        products = products.filter(
            category__iexact=category
        )

    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    else:
        products = products.order_by("-created_at")

    return render(
        request,
        "store/shop.html",
        {
            "products": products,
            "search": search,
            "sort": sort,
            "category": category,
        }
    )


# =========================================================
# PRODUCT DETAIL
# =========================================================

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product
        }
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(request, product_id):

    if not request.user.is_authenticated:
        return redirect("login")

    product = Product.objects.get(id=product_id)

    quantity = int(request.GET.get("quantity", 1))

    cart_item = CartItem.objects.filter(
        user=request.user,
        product=product,
    ).first()

    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        CartItem.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
        )

    return redirect("cart")


# =========================================================
# BUY NOW
# =========================================================

def buy_now(request, product_id):

    if not request.user.is_authenticated:
        return redirect("login")

    product = Product.objects.get(id=product_id)

    quantity = int(request.GET.get("quantity", 1))

    CartItem.objects.filter(
        user=request.user
    ).delete()

    CartItem.objects.create(
        user=request.user,
        product=product,
        quantity=quantity,
    )

    return redirect("checkout")


# =========================================================
# CART
# =========================================================

def cart(request):

    if not request.user.is_authenticated:
        return redirect("login")

    cart_items = CartItem.objects.filter(
        user=request.user
    ).order_by("-added_at")

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        "store/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        },
    )


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart(request, item_id):

    if not request.user.is_authenticated:
        return redirect("login")

    item = CartItem.objects.filter(
        id=item_id,
        user=request.user,
    ).first()

    if item:
        item.delete()

    return redirect("cart")


# =========================================================
# UPDATE CART QUANTITY
# =========================================================

def update_cart_quantity(request, item_id, action):

    if not request.user.is_authenticated:
        return redirect("login")

    item = CartItem.objects.filter(
        id=item_id,
        user=request.user,
    ).first()

    if not item:
        return redirect("cart")

    if action == "increase":

        item.quantity += 1
        item.save()

    elif action == "decrease":

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    return redirect("cart")


# =========================================================
# CHECKOUT
# =========================================================

def checkout(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart_items = CartItem.objects.filter(
        user=request.user
    ).order_by("-added_at")

    if not cart_items.exists():
        return redirect("cart")

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        pin_code = request.POST.get("pin_code", "").strip()
        payment_method = request.POST.get(
           "payment_method",
           "Online Payment"
      )
        # VALIDATION

        if not all([
            full_name,
            email,
            phone,
            address,
            city,
            pin_code,
        ]):
            return render(
                request,
                "store/checkout.html",
                {
                    "cart_items": cart_items,
                    "total": total,
                    "error": "Please fill in all delivery details.",
                },
            )

        if not phone.isdigit() or len(phone) != 10:
            return render(
                request,
                "store/checkout.html",
                {
                    "cart_items": cart_items,
                    "total": total,
                    "error": "Please enter a valid 10-digit phone number.",
                },
            )

        if not pin_code.isdigit() or len(pin_code) != 6:
            return render(
                request,
                "store/checkout.html",
                {
                    "cart_items": cart_items,
                    "total": total,
                    "error": "Please enter a valid 6-digit PIN code.",
                },
            )

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            pin_code=pin_code,
            total_amount=total,
            payment_method=payment_method,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        cart_items.delete()

        return redirect("order_success")

    return render(
        request,
        "store/checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
        },
    )


# =========================================================
# ORDER SUCCESS
# =========================================================

def order_success(request):

    return render(
        request,
        "store/success.html"
    )


# =========================================================
# WISHLIST
# =========================================================

def wishlist(request):

    if not request.user.is_authenticated:
        return redirect("login")

    wishlist_items = WishlistItem.objects.filter(
        user=request.user
    ).order_by("-added_at")

    return render(
        request,
        "store/wishlist.html",
        {
            "wishlist_items": wishlist_items,
        },
    )


# =========================================================
# ADD TO WISHLIST
# =========================================================

def add_to_wishlist(request, product_id):

    if not request.user.is_authenticated:
        return redirect("login")

    product = Product.objects.get(id=product_id)

    wishlist_item = WishlistItem.objects.filter(
        user=request.user,
        product=product,
    ).first()

    if not wishlist_item:

        WishlistItem.objects.create(
            user=request.user,
            product=product,
        )

    return redirect("wishlist")


# =========================================================
# REMOVE FROM WISHLIST
# =========================================================

def remove_from_wishlist(request, item_id):

    if not request.user.is_authenticated:
        return redirect("login")

    item = WishlistItem.objects.filter(
        id=item_id,
        user=request.user,
    ).first()

    if item:
        item.delete()

    return redirect("wishlist")


# =========================================================
# WISHLIST -> ADD TO CART
# =========================================================

def wishlist_add_to_cart(request, item_id):

    if not request.user.is_authenticated:
        return redirect("login")

    wishlist_item = WishlistItem.objects.filter(
        id=item_id,
        user=request.user,
    ).first()

    if wishlist_item:

        product = wishlist_item.product

        cart_item = CartItem.objects.filter(
            user=request.user,
            product=product,
        ).first()

        if cart_item:

            cart_item.quantity += 1
            cart_item.save()

        else:

            CartItem.objects.create(
                user=request.user,
                product=product,
                quantity=1,
            )

        wishlist_item.delete()

    return redirect("cart")


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid email or password."
            },
        )

    return render(
        request,
        "accounts/login.html",
    )


# =========================================================
# SIGNUP
# =========================================================

def signup_view(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password check
        if password != confirm_password:

            return render(
                request,
                "accounts/signup.html",
                {
                    "error": "Passwords do not match."
                },
            )

        # Email already exists check
        if User.objects.filter(username=email).exists():

            return render(
                request,
                "accounts/signup.html",
                {
                    "error": "An account with this email already exists."
                },
            )

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
        )

        # Login immediately after signup
        login(request, user)

        return redirect("home")

    return render(
        request,
        "accounts/signup.html",
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    return redirect("home")


# =========================================================
# ACCOUNT
# =========================================================

def account_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(
        request,
        "accounts/account.html",
    )
def my_orders(request):

    if not request.user.is_authenticated:
        return redirect("login")

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "accounts/orders.html",
        {
            "orders": orders,
        },
    )