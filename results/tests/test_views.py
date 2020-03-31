from django.forms.models import model_to_dict

from results.models import Country
from results.tests.base import BaseModelTestCase, BaseViewTest
from results.serializers.results_serializers import ResultSerializer
from results.constants import (
    TEST_DATA,
    TEST_SCORES,
    TEST_LINES,
    TEST_RESULTS,
    TEST_POST_RESPONSE,
    TEST_REQUEST_DATA,
    TEST_SCORES_RESULTS,
    THREAD_NAMES_DEFAULT,
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


class PostViewTest(BaseViewTest, BaseModelTestCase):
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


class TestFunctions(BaseViewTest):
    def setUp(self):
        # super().setUp()
        self.values, self.threads_ran = self.view.get_stores(TEST_REQUEST_DATA)

    def test_first_team_wins(self):
        self.assertEqual(
            True,
            self.view.first_team_wins(TEST_SCORES['first'])
        )

    def test_second_team_wins(self):
        self.assertEqual(
            False,
            self.view.first_team_wins(TEST_SCORES['second'])
        )

    def test_first_team_wins_on_away_goals(self):
        self.assertEqual(
            True,
            self.view.first_team_wins(TEST_SCORES['third'])
        )

    def test_second_team_wins_on_away_goals(self):
        self.assertEqual(
            False,
            self.view.first_team_wins(TEST_SCORES['fourth'])
        )

    def test_process_score_first_team_wins(self):
        self.assertEqual(
            TEST_RESULTS['first'],
            self.view.process_score(TEST_LINES['first'])
        )

    def test_process_score_second_team_wins(self):
        self.assertEqual(
            TEST_RESULTS['second'],
            self.view.process_score(TEST_LINES['second'])
        )

    def test_get_scores_results(self):
        # res, _ = self.view.get_stores(TEST_REQUEST_DATA)
        self.assertEqual(self.values, TEST_SCORES_RESULTS)

    def test_get_scores_threads_ran(self):
        thread_names_set = set([x.getName() for x in self.threads_ran])
        thread_names_default = set(THREAD_NAMES_DEFAULT)
        self.assertEqual(
            thread_names_default,
            thread_names_default & thread_names_set
        )
