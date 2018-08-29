from django.urls import path, include
from rest_framework.routers import DefaultRouter

from keywords.views import KeywordViewSet

app_name = 'keywords'


router = DefaultRouter()
router.register('words', KeywordViewSet, base_name='keywords')

urlpatterns = [
    path('', include(router.urls)),
]
