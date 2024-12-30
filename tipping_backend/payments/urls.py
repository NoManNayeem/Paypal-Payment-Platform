from django.urls import path
from .views import (
    PaymentHistoryView,
    initiate_paypal_payment,
    paypal_payment_success,
    paypal_payment_cancel
)

urlpatterns = [
    path('history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('paypal/initiate/', initiate_paypal_payment, name='initiate-paypal-payment'),
    path('paypal/success/', paypal_payment_success, name='paypal-payment-success'),
    path('paypal/cancel/', paypal_payment_cancel, name='paypal-payment-cancel'),
]
