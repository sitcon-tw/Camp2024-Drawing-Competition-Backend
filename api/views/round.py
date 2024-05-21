from api.models import Round, Challenge
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers.round import RoundGeneralSerializer, RoundChallengeSerializer


class RoundListCreateAPIView(APIView):  # 列出所有回合
    def get(self, request):
        round = Round.objects.filter(is_valid=True).last()
        if not round:
            return Response(
                None,
                status=404,
            )
        else:
            serializer = RoundChallengeSerializer(round)
            return Response(serializer.data)


class RoundAPIView(generics.RetrieveAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundGeneralSerializer
