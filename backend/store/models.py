from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from . import validators


class Game(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

class Account(models.Model):
    name_account = models.CharField(max_length=255)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    decription = models.TextField()

    price = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1)])
    
    image = models.ImageField(
        validators=[validators.validate_file_size],  
        upload_to='store/images',
        null=True,
        blank=True)
    def __str__(self) -> str:
        return self.name_account
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='items')
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='orderitems')
    class Meta:
        unique_together = [['order', 'account']]


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['cart', 'account']]


class Comment(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
