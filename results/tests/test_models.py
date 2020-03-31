from django.core.validators import ValidationError

from results.tests.base import BaseModelTestCase
from results.serializers.results_serializers import ResultSerializer
from results.models import Country
from results.constants import (
    TEST_DATA,
)


class CountryModelTest(BaseModelTestCase):
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
