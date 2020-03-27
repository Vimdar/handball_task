from django.forms.models import model_to_dict
from django.test import TestCase, Client
from results.models import Country
from django.core.validators import ValidationError
from results.serializers.results_serializers import ResultSerializer
from results.viewsets.handball_viewsets import ResultListView
from results.constants import (
    TEST_DATA,
    TEST_SCORES,
    TEST_LINES,
    TEST_RESULTS,
    EXAMPLE_LISTING,
    TEST_POST_DATA,
    TEST_POST_RESPONSE,
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


class CountryModelTest(BaseModelTestCase):
    # def test_created_properly(self):
    #     self.assertEqual(
    #         self.country.country_name,
    #         TEST_DATA['first_country']['country_name']
    #     )
    #     self.assertEqual(self.country.wins, TEST_DATA['first_country']['wins'])
    #     self.assertEqual(
    #         self.country.opponents,
    #         TEST_DATA['first_country']['opponents']
    #     )

    def test_country_name_length(self):
        long_name = 'x'*120
        country = self.create_country(long_name, 1, ['Belarus'])
        with self.assertRaises(ValidationError):
            country.full_clean()


class SerializerTest(BaseModelTestCase):
    def setUp(self):
        self.no_results_country = {
            'country_name': 'no results country',
            'opponents': [],
        }

    def test_proper_serialize(self):
        # no pks are serialized
        self.assertEqual(
            ResultSerializer(self.country).data,
            TEST_DATA['first_country']
        )

    def test_serializer_save_empty_country(self):
        ser = ResultSerializer(data=self.no_results_country)
        self.assertEqual(True, ser.is_valid())
        self.assertEqual(
            ser.save(),
            Country.objects.filter(country_name='no results country').first()
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
