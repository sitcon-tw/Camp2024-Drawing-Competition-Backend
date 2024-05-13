from api.models import Submission
from rest_framework import serializers


class SubmissionGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ("id",)