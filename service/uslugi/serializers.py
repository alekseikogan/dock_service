from rest_framework import serializers

from .models import Subscription, Plan, Client

class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ('plan_type', 'discount_percent',)


class SubscriptionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.user.username')
    client_company_name = serializers.CharField(source='client.company_name')
    plan = PlanSerializer(read_only=True)
    sell_price = serializers.SerializerMethodField(read_only=True)

    def get_sell_price(self, instance):
        return instance.sell_price

    class Meta:
        model = Subscription
        fields = ('id', 'client_name', 'client_company_name', 'plan', 'sell_price')