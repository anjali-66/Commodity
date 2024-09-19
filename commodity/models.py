from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, user_type=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not user_type:
            raise ValueError('Users must have a user type')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type='lender',  # or 'admin' if you create an admin type
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# User Model
class User(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ('renter', 'Renter'),
        ('lender', 'Lender'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.user_type == 'lender'

# Products Model
class Products(models.Model):
    CATEGORY_CHOICES = (
        ('Electronic Appliances', 'Electronic Appliances'),
        ('Electronic Accessories', 'Electronic Accessories'),
        ('Furniture', 'Furniture'),
        ('Men’s wear', 'Men’s wear'),
        ('Women’s wear', 'Women’s wear'),
        ('Shoes', 'Shoes'),
    )

    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    quote_price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    item_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    is_rented = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name

# Bid Model
class Bid(models.Model):
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    Products = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='bids')
    bid_price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    bid_duration = models.IntegerField()  # in months
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Bid by {self.renter.email} on {self.Products.item_name}'

# Rental Agreement Model
class RentalAgreement(models.Model):
    Products = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='rental_agreements')
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_agreements')
    rental_start_date = models.DateField()
    rental_end_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Rental Agreement for {self.Products.item_name} by {self.renter.email}'
