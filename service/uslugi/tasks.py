from celery import shared_task


@shared_task
def count_price(subscription_id):
    from .models import Subscription
    subscription = Subscription.objects.get(id=subscription_id)
    sell_price = subscription.service.price * (1 - subscription.plan.discount_percent / 100.00)
    subscription.price = sell_price
    subscription.save(save_model=False)