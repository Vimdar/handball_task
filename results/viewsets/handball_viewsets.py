import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from multiprocessing.queues import Empty
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response

from results.models import Country
from results.serializers.results_serializers import ResultSerializer


class ResultListView(ListCreateAPIView, GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = ResultSerializer
    ordering_fields = ('wins', 'country_name')
    ordering = ('-wins', 'country_name')
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter
    )

# curl -i -H "Content-Type: application/json" -X POST
# --data '{"data": "Denmark | Belgium | 0:0 | 1:1\nBelgium | Austria | 2:0 | 0:2\nLatvia | Monaco | 2:0 | 0:0\nBulgaria | Italy | 2:1 | 3:2\nstop"}'
# http://localhost:8000/results_endpoint/
    def create(self, request, *args, **kwargs):
        data = request.data['data'].split('\n')
        # data guaranteed ends up with a stop line we do not need
        stores = [self.process_score(x) for x in data[:-1]]
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

    def process_score(self, line):
        line = line.split('|')
        line = [x.strip() for x in line]
        scores = line[2:]
        home_team_name, away_team_name = line[:2]
        first_wins = self.first_team_wins(scores)
        results = (
                        {'country_name': home_team_name,
                         'opponents': [away_team_name]
                         },
                        {'country_name': away_team_name,
                         'opponents': [home_team_name]
                         }
                    )
        if first_wins:
            results[0]['wins'] = 1
            results[1]['wins'] = 0
        else:
            results[0]['wins'] = 0
            results[1]['wins'] = 1
        return results

    def first_team_wins(self, scores):
        scores = [x.split(':') for x in scores]
        first_team_goals = scores[0][0], scores[1][1]
        second_team_goals = scores[0][1], scores[1][0]
        first_team_goals = [int(x) for x in first_team_goals]
        second_team_goals = [int(x) for x in second_team_goals]
        if sum(first_team_goals) > sum(second_team_goals):
            return True
        elif sum(second_team_goals) > sum(first_team_goals):
            return False
        else:
            return first_team_goals[1] > second_team_goals[0]
