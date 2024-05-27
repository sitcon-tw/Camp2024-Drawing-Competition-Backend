import datetime

from django.utils import timezone
from api.models import Round, Challenge
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers.round import RoundGeneralSerializer, RoundChallengeSerializer


class RoundListAPIView(APIView):  # 列出所有回合
    def get(self, request):
        # 比較當前時間進行到哪一個回合
        now = timezone.now()
        round = Round.objects.filter(start_time__lte=now, end_time__gte=now).last()
        if round:
            # 標註該 Round 已經進行過了
            round.is_valid = True
            round.save()
            serializer = RoundChallengeSerializer(round)
            return Response(serializer.data)
        # 檢查是否所有回合結束
        elif not Round.objects.filter(is_valid=True).exists():
            return Response(
                None,
                status=status.HTTP_204_NO_CONTENT,
            )
        # 檢查是否沒有開放回合
        elif not round:
            return Response(
                None,
                status=status.HTTP_404_NOT_FOUND,
            )


class RoundAPIView(generics.RetrieveAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundGeneralSerializer
