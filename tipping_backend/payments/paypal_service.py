import paypalrestsdk
from django.conf import settings

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_CONFIG["mode"],  # sandbox or live
    "client_id": settings.PAYPAL_CONFIG["client_id"],
    "client_secret": settings.PAYPAL_CONFIG["client_secret"],
})

def create_paypal_payment(amount, description, return_url, cancel_url):
    """
    Create a PayPal payment.
    """
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": f"{amount:.2f}",
                "currency": "USD"
            },
            "description": description
        }],
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url
        }
    })
    if payment.create():
        return payment
    else:
        raise Exception(payment.error)
