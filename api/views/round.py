from api.models import Round
from rest_framework import generics

from api.serializers.round import (
    RoundGeneralSerializer,
)


class RoundListCreateAPIView(generics.ListAPIView):  # 列出所有回合
    queryset = Round.objects.all()
    serializer_class = RoundGeneralSerializer


class RoundAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundGeneralSerializer
