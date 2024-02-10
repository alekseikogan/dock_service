from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch, F, Sum
from .serializers import SubscriptionSerializer
from .models import Subscription, Client


class SubscriptionView(ReadOnlyModelViewSet):
    # queryset = Subscription.objects.all().prefetch_related(
    #     'client', 'plan').only(
    #         'client__company_name',
    #         'plan__plan_type',
    #         'plan__discount_percent'
    #         ).prefetch_related('client__user')
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch(
            'client',
            queryset=Client.objects.all().select_related('user').only(
                'user__username',
                'company_name')
        )
    ).annotate(sell_price=F('service__price') * (1 - F('plan__discount_percent') / 100.00))
    serializer_class = SubscriptionSerializer

    # вот так лущче не делать, но если бизнес-логика требует
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        response_data = {'result': response.data}
        response_data['total_price'] = queryset.aggregate(total=Sum('sell_price'))['total']
        response.data = response_data
        return response