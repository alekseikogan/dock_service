from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F


@shared_task(base=Singleton)
def count_price(subscription_id):
    from .models import Subscription
    subscription = Subscription.objects.filter(id=subscription_id).annotate(
        annotated_price=F('service__price') * (1 - F('plan__discount_percent') / 100.00)).first()
    subscription.price = subscription.annotated_price
    subscription.save()