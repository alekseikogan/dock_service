from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch, Sum
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
        ))
    serializer_class = SubscriptionSerializer

    # вот так лущче не делать, но если бизнес-логика требует
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        response_data = {'result': response.data}
        response_data['total_price'] = queryset.aggregate(total=Sum('price'))['total']
        response.data = response_data
        return response