from api.models import Round, Challenge
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers.round import RoundGeneralSerializer, RoundChallengeSerializer


class RoundListCreateAPIView(APIView):  # 列出所有回合
    def get(self, request):
        rounds = Round.objects.filter(is_valid=True)
        if rounds.count() == 0:
            return Response(
                None,
                status=404,
            )
        else:
            serializer = RoundChallengeSerializer(rounds, many=True)
            return Response(serializer.data)


class RoundAPIView(generics.RetrieveAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundGeneralSerializer
