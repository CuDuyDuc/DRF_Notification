from notification_be.apps.models_container import models, User, Product
import uuid
from notification_be.apps.enum_container import Status

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.PositiveIntegerField(default=0)
    total_money = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.name) for tag in Status],  # Chuyển Enum thành tuple (value, name)
        default=Status.PENDING.value,  # Mặc định là 'pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart')
    objects = models.Manager()

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'