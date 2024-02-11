import datetime
import time
from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F
from django.db import transaction

@shared_task(base=Singleton)
def count_price(subscription_id):
    '''A task that counts the price for a subscription based on the given subscription ID.'''
    from .models import Subscription

    with transaction.atomic():
        time.sleep(5)

        subscription = Subscription.objects.select_for_upadate().filter(id=subscription_id).annotate(
            annotated_price=F('service__price') * (1 - F('plan__discount_percent') / 100.00)).first()
        
        time.sleep(10)

        subscription.price = subscription.annotated_price
        subscription.save()


@shared_task(base=Singleton)
def set_comment(subscription_id):
    from .models import Subscription

    with transaction.atomic():
        # возьмет первым Подписку и не даст никому пользоваться
        subscription = Subscription.objects.select_for_upadate().get(id=subscription_id)
        time.sleep(18)

        subscription.comment = str(datetime.datetime.now())
        subscription.save()
        # после осободит запись Подписки с данным ID