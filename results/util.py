import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.queues import Empty
from queue import Queue


class EnumThreadPoolExecutor(ThreadPoolExecutor):
    def __init__(
        self,
        max_workers=None,
        thread_name_prefix='',
        initializer=None,
        initargs=()
    ):
        super().__init__(
            max_workers=None,
            thread_name_prefix='',
            initializer=None,
            initargs=()
        )
        self._threads_run = []

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._threads_run += threading.enumerate()
        self.shutdown(wait=True)
        return False

    def get_threads_run(self):
        return self._threads_run


def process_score(line):
    line = line.split('|')
    line = [x.strip() for x in line]
    scores = line[2:]
    home_team_name, away_team_name = line[:2]
    first_wins = first_team_wins(scores)
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


def first_team_wins(scores):
    scores = [x.split(':') for x in scores]
    first_team_goals = scores[0][0], scores[1][1]
    second_team_goals = scores[0][1], scores[1][0]
    first_team_goals = [int(x) for x in first_team_goals]
    second_team_goals = [int(x) for x in second_team_goals]
    if sum(first_team_goals) > sum(second_team_goals):
        return True
    if sum(second_team_goals) > sum(first_team_goals):
        return False
    return first_team_goals[1] > second_team_goals[0]


def calc_thread(queue):
    # ...and a second thread that takes the input lines one by one from
    # the same structure and makes the needed calculations...
    threading.current_thread().name = 'calc_thread'
    rows_left = 1
    res = []
    while rows_left:
        try:
            row = queue.get(False)
            res.append(process_score(row['row']))
            rows_left = row['rows_left']
        except Empty:
            # print('Nothing in queue...')
            pass
    return res


def read_thread(data, queue):
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


def get_stores(data):
    qq = Queue()
    # adding threading part of the task with python concurrent.futures module
    # and a python built-in Queue (since our task is not very heavy and time-consuming)
    # instead of having lots of additional overhead from using another asynchronous
    # task job package for background jobs (e.g. celery, etc.) and additional message
    # broker
    with EnumThreadPoolExecutor(max_workers=2) as prod:
        f2 = prod.submit(calc_thread, qq)
        prod.submit(read_thread, data, qq)
        stores = f2.result()
    return stores, prod.get_threads_run()
