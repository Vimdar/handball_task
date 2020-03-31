from django.forms.models import model_to_dict

from results.models import Country
from results.tests.base import BaseModelTestCase, BaseViewTest
from results.serializers.results_serializers import ResultSerializer
from results.constants import (
    TEST_DATA,
    TEST_POST_RESPONSE,
)


class ListViewTest(BaseViewTest, BaseModelTestCase):

    def test_status_codes(self):
        self.assertEqual(self.main_resp.status_code, 200)
        self.assertEqual(self.results_enpoint_resp.status_code, 200)

    def test_list(self):
        res = self.client.get('/results_endpoint/')
        self.assertEqual(res.data['count'], 1)
        self.assertEqual(dict(res.data['results'][0]), TEST_DATA['first_country'])


class SimpleUpsertTest(BaseViewTest, BaseModelTestCase):
    def setUp(self):
        self.view.perform_simple_upsert(
            ResultSerializer(data=TEST_DATA['second_country'])
        )
        self.view.perform_simple_upsert(
            ResultSerializer(data=TEST_DATA['third_country'])
        )

    def test_simple_upsert_update(self):
        updated = model_to_dict(
            Country.objects.filter(country_name='Bulgaria').first()
        )
        del updated['country_id']
        self.assertEqual(updated, TEST_DATA['fourth_country'])

    def test_simple_upsert_insert(self):
        updated = model_to_dict(
            Country.objects.filter(country_name='Italy').first()
        )
        del updated['country_id']
        self.assertEqual(updated, TEST_DATA['second_country'])


class PostViewTest(BaseModelTestCase):
    def setUp(self):
        country_Italy = self.create_country(**TEST_DATA['second_country'])
        country_Italy.save()
        self.res_1 = self.client.post(
            '/results_endpoint/',
            data={'data': 'Bulgaria | Netherlands | 5:0 | 0:1\nstop'}
        )
        # Italy should get a loss with these scores
        self.res_2 = self.client.post(
            '/results_endpoint/',
            data={'data': 'England | Italy | 0:0 | 1:1\nstop'}
        )

    def test_post_response(self):
        self.assertEqual(self.res_1.status_code, 201)
        self.assertEqual(TEST_POST_RESPONSE, self.res_1.data)

    def test_updated_win(self):
        updated = model_to_dict(
            Country.objects.filter(country_name='Bulgaria').first()
        )
        del updated['country_id']
        self.assertEqual(updated, TEST_DATA['fourth_country'])

    def test_inserted_loss(self):
        inserted = model_to_dict(
            Country.objects.filter(country_name='Netherlands').first()
        )
        del inserted['country_id']
        self.assertEqual(inserted, TEST_DATA['fifth_country'])

    def test_updated_loss(self):
        updated = model_to_dict(
            Country.objects.filter(country_name='Italy').first()
        )
        del updated['country_id']
        self.assertEqual(updated, TEST_DATA['sixth_country'])

    def test_inserted_win(self):
        inserted = model_to_dict(
            Country.objects.filter(country_name='England').first()
        )
        del inserted['country_id']
        self.assertEqual(inserted, TEST_DATA['seventh_country'])
