from django.conf.urls import include, url
from results import urls as results_urls

urlpatterns = [
    url(r'^', include(results_urls)),
]
