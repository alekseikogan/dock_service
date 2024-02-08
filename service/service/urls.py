from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from uslugi.views import SubscriptionView

router = routers.DefaultRouter()
router.register(r'api/subscriptions/', SubscriptionView, basename='subscriptions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]