from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Product(models.Model):
    SIZE_TYPE_CHOICES = [
        ('Обувь', 'Обувь'),
        ('Джинсы', 'Джинсы'),
        ('Футболка', 'Футболка'),
    ]

    GENDER_CHOICES = [
        ('Мужчины', 'Мужчины'),
        ('Женщины', 'Женщины'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    size_type = models.CharField(max_length=50, choices=SIZE_TYPE_CHOICES, default='Футболка')
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='Мужчины')  # Поле для указания пола

    # Мужские размеры
    shoes_size_men_39 = models.IntegerField(default=0, blank=True, null=True)
    shoes_size_men_40 = models.IntegerField(default=0, blank=True, null=True)
    shoes_size_men_41 = models.IntegerField(default=0, blank=True, null=True)
    shoes_size_men_42 = models.IntegerField(default=0, blank=True, null=True)
    shoes_size_men_43 = models.IntegerField(default=0, blank=True, null=True)
    shoes_size_men_44 = models.IntegerField(default=0, blank=True, null=True)

    # Женские размеры
    shoes_size_women_35 = models.IntegerField(default=0, blank=True, null=True)
    shoes_size_women_36 = models.IntegerField(default=0, blank=True, null=True)
    shoes_size_women_37 = models.IntegerField(default=0, blank=True, null=True)
    shoes_size_women_38 = models.IntegerField(default=0, blank=True, null=True)
    shoes_size_women_39 = models.IntegerField(default=0, blank=True, null=True)
    shoes_size_women_40 = models.IntegerField(default=0, blank=True, null=True)

    # Размеры одежды для мужчин и женщин
    shirt_size_s = models.IntegerField(default=0, blank=True, null=True)
    shirt_size_m = models.IntegerField(default=0, blank=True, null=True)
    shirt_size_l = models.IntegerField(default=0, blank=True, null=True)
    shirt_size_xl = models.IntegerField(default=0, blank=True, null=True)
    shirt_size_xxl = models.IntegerField(default=0, blank=True, null=True)

    # Размеры Джинсы для мужчин и женщин
    jeans_size_40 = models.IntegerField(default=0, blank=True, null=True)
    jeans_size_42 = models.IntegerField(default=0, blank=True, null=True)
    jeans_size_44 = models.IntegerField(default=0, blank=True, null=True)
    jeans_size_46 = models.IntegerField(default=0, blank=True, null=True)
    jeans_size_48 = models.IntegerField(default=0, blank=True, null=True)
    jeans_size_50 = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)  # Например, размер обуви, футболки и т.д.
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    added_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.product.name} - {self.size} ({self.quantity})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name}'