from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .viewsets.handball_viewsets import ResultListView

router = DefaultRouter()
raw_items = router.register(
    r'results_endpoint',
    ResultListView,
    basename='results_raw'
)

urlpatterns = [
    url(r'^', include(router.urls)),
]
