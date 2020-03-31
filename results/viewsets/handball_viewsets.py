from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response

from results.models import Country
from results.serializers.results_serializers import ResultSerializer
from results.util import (
    get_stores,
)


class ResultListView(ListCreateAPIView, GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = ResultSerializer
    ordering_fields = ('wins', 'country_name')
    ordering = ('-wins', 'country_name')
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter
    )

    def create(self, request):
        data = request.data
        stores, _ = get_stores(data)
        stores_flat = [x for pair in stores for x in pair]
        records = [self.get_serializer(data=x) for x in stores_flat]
        for record in records:
            self.perform_simple_upsert(record)

        return Response(
            [rec.data for rec in records],
            status=HTTP_201_CREATED,
        )

    def perform_simple_upsert(self, row):
        # no need to keep more complicated track of so called dirty fields
        presented = self.queryset.filter(
            country_name=row.initial_data['country_name']
        )
        # do not raise exceptions on is_valid since our input must be OK
        if row.is_valid():
            if not presented:
                self.perform_create(row)
            else:
                country_ins = presented.first()
                country_ins.wins += row.data['wins']
                country_ins.opponents += row.data['opponents']
                country_ins.save()
