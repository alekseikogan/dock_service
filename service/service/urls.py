from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from uslugi.views import SubscriptionView
from .settings import DEBUG

router = routers.DefaultRouter()
router.register(r'api/subscriptions', SubscriptionView, basename='subscriptions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]

if DEBUG:
    urlpatterns += [
    path("__debug__/", include("debug_toolbar.urls")),
]