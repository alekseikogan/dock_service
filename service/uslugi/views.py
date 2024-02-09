from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch
from .serializers import SubscriptionSerializer
from .models import Subscription, Client


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'client', 'plan').only(
            'client__company_name',
            'plan__plan_type',
            'plan__discount_percent'
            ).prefetch_related('client__user')
    # queryset = Subscription.objects.all().prefetch_related(
    #     Prefetch(
    #         'client',
    #         queryset=Client.objects.all().only('company_name')
    #     )
    # )
    serializer_class = SubscriptionSerializer
