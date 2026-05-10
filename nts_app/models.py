from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)  # Add this line

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Category')
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)   # Brand field
    storage = models.CharField(max_length=50)  # Storage field (e.g., 256GB, 512GB)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product/',blank=True)

    def __str__(self):
        return f"{self.name} {self.category.name}"

@staticmethod
def get_all_products():
    return Product.objects.all()

@property
def discount_percentage(self):
        if self.offer_price:
            return int(((self.price - self.offer_price) / self.price) * 100)
        return 0

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    upi_id = models.CharField(max_length=100, null=True, blank=True)  # ✅ add this

    def __str__(self):
        return self.product.name


    @property
    def total(self):
        return self.product.price * self.quantity


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # same product repeat na ho

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"