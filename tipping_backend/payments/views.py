from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import PaymentHistory
from .serializers import PaymentHistorySerializer
from accounts.models import CustomUser
from .filters import PaymentHistoryFilter
from .paypal_service import create_paypal_payment
import paypalrestsdk
import logging

# Set up logging
logger = logging.getLogger(__name__)


class PaymentHistoryView(generics.ListAPIView):
    """
    List Payment History with advanced filtering, search, and pagination.
    """
    queryset = PaymentHistory.objects.all().order_by('-created_at')
    serializer_class = PaymentHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PaymentHistoryFilter
    search_fields = ['transaction_id', 'customer__username']

    def get_queryset(self):
        """
        Filter queryset based on user role.
        """
        user = self.request.user
        if user.role == 'customer':
            # Customers see only their own payments
            return PaymentHistory.objects.filter(customer=user)
        elif user.role == 'restaurant_owner':
            # Restaurant owners see all payments
            return PaymentHistory.objects.all()
        return PaymentHistory.objects.none()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def initiate_paypal_payment(request):
    """
    Initiate a PayPal payment.
    """
    try:
        user = request.user if request.user.is_authenticated else None
        data = request.data
        staff = get_object_or_404(CustomUser, id=data.get('staff_id'), role='staff')
        amount = float(data.get('amount'))
        description = f"Tip for {staff.username}"

        # Generate PayPal payment
        payment = create_paypal_payment(
            amount=amount,
            description=description,
            return_url=f"http://127.0.0.1:8000/api/payments/paypal/success/?staff_id={staff.id}&amount={amount}&customer_id={user.id if user else ''}",
            cancel_url="http://127.0.0.1:8000/api/payments/paypal/cancel/"
        )

        # Get approval URL
        for link in payment.links:
            if link.rel == "approval_url":
                logger.info("Payment initiated successfully.")
                return Response({"approval_url": link.href})

        logger.error("Approval URL not found in PayPal response.")
        return Response({"error": "Unable to generate PayPal approval URL."}, status=500)

    except Exception as e:
        logger.exception("Error initiating PayPal payment:")
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def paypal_payment_success(request):
    """
    Handle PayPal payment success.
    """
    try:
        staff_id = request.GET.get('staff_id')
        amount = request.GET.get('amount')
        payer_id = request.GET.get('PayerID')
        payment_id = request.GET.get('paymentId')
        customer_id = request.GET.get('customer_id')

        # Execute the PayPal payment
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            staff = get_object_or_404(CustomUser, id=staff_id, role='staff')
            customer = get_object_or_404(CustomUser, id=customer_id) if customer_id else None
            transaction_id = payment.id

            # Create a record in the PaymentHistory model
            PaymentHistory.objects.create(
                customer=customer,
                staff=staff,
                amount=amount,
                transaction_id=transaction_id,
                status='success'
            )

            logger.info("Payment executed successfully.")
            return Response({"message": "Payment successful!", "transaction_id": transaction_id})
        else:
            logger.error("Payment execution failed.")
            return Response({"error": "Payment execution failed."}, status=400)

    except paypalrestsdk.ResourceNotFound:
        logger.error("Invalid PayPal payment ID.")
        return Response({"error": "Invalid payment ID."}, status=404)
    except Exception as e:
        logger.exception("Error handling PayPal payment success:")
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def paypal_payment_cancel(request):
    """
    Handle PayPal payment cancellation.
    """
    try:
        staff_id = request.GET.get('staff_id')
        amount = request.GET.get('amount')

        logger.info(f"Payment canceled. Staff ID: {staff_id}, Amount: {amount}")
        return Response({"message": "Payment was canceled by the user."})
    except Exception as e:
        logger.exception("Error handling PayPal payment cancellation:")
        return Response({"error": str(e)}, status=400)
