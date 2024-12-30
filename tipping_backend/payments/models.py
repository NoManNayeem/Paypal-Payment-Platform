from django.db import models
from accounts.models import CustomUser

class PaymentHistory(models.Model):
    customer = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='payments',
        limit_choices_to={'role': 'customer'}
    )
    staff = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='tips',
        limit_choices_to={'role': 'staff'}
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, choices=[('success', 'Success'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
