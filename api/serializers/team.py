from api.models import Team
from rest_framework import serializers


class TeamGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"
        read_only_fields = ("id",)