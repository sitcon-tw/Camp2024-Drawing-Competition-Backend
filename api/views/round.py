import logging

from api.models import Round
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.round import (
    RoundGeneralSerializer,
)

class RoundListCreateAPIView(generics.ListCreateAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundGeneralSerializer

    
class RoundAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundGeneralSerializer
