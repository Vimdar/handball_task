from django.db.models import (
    AutoField,
    Model,
    IntegerField,
    CharField,
)
from django.contrib.postgres.fields import ArrayField


class Country(Model):
    # still define a pk field over django's default id
    country_id = AutoField(primary_key=True)
    country_name = CharField(max_length=100, unique=True)
    wins = IntegerField()
    opponents = ArrayField(
        CharField(max_length=100, blank=True, default=''),
        # last 20 opponents will be saved
        default=list,
        size=20,
        blank=True,
        null=True,
    )
