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

    def create(self, request, *args, **kwargs):
        data = request.data
        qq = Queue()
        # adding threading part of the task with python concurrent.futures module
        # and a python built-in Queue (since our task is not very heavy and time-consuming)
        # instead of having lots of additional overhead from using another asynchronous
        # task job package for background jobs (e.g. celery, etc.) and additional message
        # broker
        with ThreadPoolExecutor(max_workers=2) as prod:
            f2 = prod.submit(self.calc_thread, qq)
            prod.submit(self.read_thread, data, qq)
            stores = f2.result()
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

    def read_thread(self, data, queue):
        # ...one to read the input line by line and to store it
        # in a data structure of your choice...
        threading.current_thread().name = 'read_thread'
        data = data['data'].split('\n')
        # data guaranteed ends up with a stop line we do not need
        data = data[:-1]
        rows_left = len(data) - 1
        for row in data:
            queue.put({'rows_left': rows_left, 'row': row})
            rows_left -= 1

    def calc_thread(self, queue):
        # ...and a second thread that takes the input lines one by one from
        # the same structure and makes the needed calculations...
        threading.current_thread().name = 'calc_thread'
        rows_left = 1
        res = []
        while rows_left:
            try:
                row = queue.get(False)
                res.append(self.process_score(row['row']))
                rows_left = row['rows_left']
            except Empty:
                # print('Nothing in queue...')
                pass
        return res

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
