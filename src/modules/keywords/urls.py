from django.urls import path, include
from rest_framework.routers import DefaultRouter

from keywords.views import KeywordViewSet, VideoItemListView

app_name = 'keywords'


router = DefaultRouter()
router.register('words', KeywordViewSet, base_name='keywords')

urlpatterns = [
    path('', include(router.urls)),
    path('words/<int:keyword_id>/video/', VideoItemListView.as_view())
]
