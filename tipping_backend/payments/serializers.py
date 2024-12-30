from rest_framework import serializers
from .models import PaymentHistory

class PaymentHistorySerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    staff_name = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()

    class Meta:
        model = PaymentHistory
        fields = ['id', 'customer_name', 'staff_name', 'branch', 'amount', 'transaction_id', 'status', 'created_at']

    def get_customer_name(self, obj):
        return obj.customer.username if obj.customer else "Anonymous"

    def get_staff_name(self, obj):
        return obj.staff.username

    def get_branch(self, obj):
        return obj.staff.branch
