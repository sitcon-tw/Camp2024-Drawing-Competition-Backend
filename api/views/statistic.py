import logging

from api.models import Team, Submission, Round
from django.db.models import Max, F
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.submission import SubmissionGeneralSerializer
from api.serializers.team import (
    TeamGeneralSerializer,
)


class TeamChallengeScoreStaticAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get the highest score of each challenge for a team",
        operation_description="Get the highest score of each challenge for a team",
        manual_parameters=[
            openapi.Parameter(
                "team_id",
                openapi.IN_QUERY,
                description="The ID of the team",
                type=openapi.TYPE_INTEGER,
            )
        ],
    )
    def get(self, request):
        team_id = request.query_params.get("team_id", None)
        # 如果 team_id 沒有被提供，則不過濾 Submission
        if team_id is None:
            submissions = Submission.objects.all()
        else:
            submissions = Submission.objects.filter(team_id=team_id)

        # 使用 annotate 來計算每個 Challenge 的最高分
        highest_scores = (
            submissions.values("challenge")
            .annotate(max_score=Max("score"))
            .values("challenge", "max_score")
        )

        # 將結果轉換為字典，方便後續處理
        result = {}
        for item in highest_scores:
            challenge = item["challenge"]
            max_score = item["max_score"]

            # 如果這個 Challenge 還沒有最高分 Submission，則新增
            if challenge not in result:
                result[challenge] = None

            # 更新或新增最高分 Submission
            result[challenge] = {
                "max_score": max_score,
                "submission": SubmissionGeneralSerializer(
                    submissions.filter(challenge=challenge, score=max_score).first()
                ).data,
            }

        return Response(result, status=status.HTTP_200_OK)
