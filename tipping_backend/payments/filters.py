import django_filters
from .models import PaymentHistory

class PaymentHistoryFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")
    branch = django_filters.CharFilter(field_name="staff__branch", lookup_expr="icontains")

    class Meta:
        model = PaymentHistory
        fields = ['staff', 'start_date', 'end_date', 'branch']
