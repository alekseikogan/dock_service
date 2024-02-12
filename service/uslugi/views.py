from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch, Sum
from .serializers import SubscriptionSerializer
from .models import Subscription, Client
from django.core.cache import cache
from service.settings import PRICE_CACHE_NAME

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
        ))
    serializer_class = SubscriptionSerializer

    # вот так лущче не делать, но если бизнес-логика требует
    # тут можно будет использовать кэширование total_price
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get(PRICE_CACHE_NAME)
        if price_cache:
            total_price_amount = price_cache
        else:
            total_price_amount = queryset.aggregate(total=Sum('price'))['total']
            cache.set(PRICE_CACHE_NAME, total_price_amount, 60 * 60)

        response_data = {'total_price': total_price_amount}
        response_data['result'] = response.data
        response.data = response_data
        return response