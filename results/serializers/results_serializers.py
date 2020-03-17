from rest_framework import serializers
from results.models import Country


class ResultSerializer(serializers.Serializer):
    # country_id = serializers.PrimaryKeyRelatedField(
    #     read_only=True,
    # )
    country_name = serializers.CharField(max_length=100)
    # store a loss if a win is not present explicitly;
    # might move this logic to view to be more explicit
    wins = serializers.IntegerField(default=0)
    opponents = serializers.ListField(
        child=serializers.CharField(max_length=100),
        allow_empty=True
    )

    class Meta:
        model = Country
        fields = ('country_name', 'wins', 'opponents')

    def create(self, validated_data):
        return Country.objects.create(**validated_data)
