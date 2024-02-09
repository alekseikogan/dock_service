from rest_framework import serializers

from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.user.username')
    client_company_name = serializers.CharField(source='client.company_name')
    plan = serializers.StringRelatedField(source='plan.plan_type', read_only=True)
    # email = serializers.EmailField(source='client.user.email')

    class Meta:
        model = Subscription
        fields = ('id', 'client_name', 'client_company_name', 'plan',)