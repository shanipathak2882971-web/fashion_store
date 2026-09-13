from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=[
            ("Men", "Men"),
            ("Women", "Women"),
            ("Collections", "Collections"),
            ("Sale", "Sale"),
       ],
       default="Men",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
class Order(models.Model):
    full_name = models.CharField(max_length=200)
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
       max_length=50,
       default="Online Payment"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
         max_length=50,
         choices=[
             ("Pending", "Pending"),
             ("Confirmed", "Confirmed"),
             ("Processing", "Processing"),
             ("Shipped", "Shipped"),
             ("Delivered", "Delivered"),
             ("Cancelled", "Cancelled"),
             ],
             default="Pending",
    )

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
class WishlistItem(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name