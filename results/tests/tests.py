from results.tests.base import BaseViewTest
from results.constants import (
    EXAMPLE_LISTING,
    TEST_POST_DATA,
)


class FirstExampleTest(BaseViewTest):
    def setUp(self):
        self.res = self.client.post(
            '/results_endpoint/',
            data={
                'data': TEST_POST_DATA['first']
            }
        )

    def test_results(self):
        res = self.client.get('/results_endpoint/')
        self.assertEqual(res.data['count'], len(EXAMPLE_LISTING['first']))
        self.assertEqual(
            [dict(x) for x in res.data['results']],
            EXAMPLE_LISTING['first']
        )


class SecondExampleTest(BaseViewTest):
    def setUp(self):
        self.res = self.client.post(
            '/results_endpoint/',
            data={
                'data': TEST_POST_DATA['second']
            }
        )

    def test_results(self):
        res = self.client.get('/results_endpoint/')
        self.assertEqual(res.data['count'], len(EXAMPLE_LISTING['second']))
        self.assertEqual(
            [dict(x) for x in res.data['results']],
            EXAMPLE_LISTING['second']
        )


class ThirdExampleTest(BaseViewTest):
    def setUp(self):
        self.res = self.client.post(
            '/results_endpoint/',
            data={
                'data': TEST_POST_DATA['third']
            }
        )

    def test_results(self):
        res = self.client.get('/results_endpoint/')
        self.assertEqual(res.data['count'], len(EXAMPLE_LISTING['third']))
        self.assertEqual(
            [dict(x) for x in res.data['results']],
            EXAMPLE_LISTING['third']
        )
