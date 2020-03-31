from django.test import TestCase, Client

from results.models import Country
from results.viewsets.handball_viewsets import ResultListView
from results.constants import (
    TEST_DATA,
)


class BaseModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseModelTestCase, cls).setUpClass()
        cls.country = cls.create_country(**TEST_DATA['first_country'])
        cls.country.save()

    @classmethod
    # instead of using factory package
    def create_country(
        self,
        country_name,
        wins,
        opponents,
    ):
        return Country(
            country_name=country_name,
            wins=wins,
            opponents=opponents
        )


class BaseViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseViewTest, cls).setUpClass()
        cls.client = Client()
        cls.view = ResultListView()

    def setUp(self):
        self.main_resp = self.client.get('/')
        self.results_enpoint_resp = self.client.get('/results_endpoint/')
