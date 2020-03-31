import threading
from concurrent.futures import ThreadPoolExecutor


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
