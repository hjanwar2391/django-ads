from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from .signals import create_user_wallet, save_user_wallet
from .managers import CustomUserManager  # Import the custom user manager
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
  


# user create
class User(AbstractUser):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('checking', 'Checking'),
        ('active', 'Active'),
    ]
    
    unique_id = models.CharField(max_length=5, unique=True, editable=False)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Remove username field and replace with email as the unique identifier
    username = None
    email = models.EmailField(unique=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    USERNAME_FIELD = 'email'  # Use email as the username
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address', 'city', 'zip_code', 'country']  # Fields required for superuser creation

    objects = CustomUserManager()  # Use the custom manager

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = str(random.randint(10000, 99999))  # Generate a unique ID
        super(User, self).save(*args, **kwargs)




# user waller
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=15)  # Default value of 15 points

    def add_points(self, points):
        self.points += points
        self.save()

    def can_withdraw(self):
        return self.points >= 450 and self.user.reference_set.count() >= 3




# admin upload video
class Ad(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to="videos/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



# user can view ad
class UserAdView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)



# admin can reference user
class Reference(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reference_set"
    )
    referred_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="referred_by_set"
    )


# admin area
class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]


class Withdrawal(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    withdrawal_method = models.CharField(
        max_length=50, choices=[("bkash", "Bkash"), ("nagad", "Nagad")]
    )
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
