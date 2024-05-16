from api.model.challenge import Challenge
from api.models import Submission
from django.db.models import Max
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.submission import SubmissionGeneralSerializer


class TeamChallengeScoreStaticAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Get the highest fitness of each challenge for a team",
        operation_description="Get the highest fitness of each challenge for a team",
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
        highest_fitness = (
            submissions.values("challenge")
            .annotate(max_fitness=Max("fitness"))
            .values("challenge", "max_fitness")
        )

        # 將結果整理與輸出
        response = []
        for item in highest_fitness:
            result = {}
            result["challenge"] = item["challenge"]
            result["max_fitness"] = item["max_fitness"]
            result["submission"] = SubmissionGeneralSerializer(
                submissions.filter(
                    challenge=item["challenge"], fitness=item["max_fitness"]
                ).first()
            ).data
            response.append(result)

        return Response(response, status=status.HTTP_200_OK)


class TeamChallengeSubmissionStaticAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get the submission count of each challenge for a team",
        operation_description="Get the submission count of each challenge for a team",
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

        result = []
        for challenge in Challenge.objects.all():
            submission_count = 0
            if team_id is None:
                submission_count = submissions.filter(challenge=challenge).count()
            else:
                submission_count = submissions.filter(
                    challenge=challenge, team_id=team_id
                ).count()
            result.append(
                {
                    "challenge": challenge.pk,
                    "submission_count": submission_count,
                }
            )

        return Response(result, status=status.HTTP_200_OK)


class TeamRoundScoreStatisticAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get the team total score in each round",
        operation_description="Get team total score in each round",
        manual_parameters=[
            openapi.Parameter(
                "team_id",
                openapi.IN_QUERY,
                description="The ID of the team",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "round_id",
                openapi.IN_PATH,
                description="The ID of the round",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def get(self, request, round_id: int):
        team_id = request.query_params.get("team_id", None)
        # 如果 team_id 沒有被提供，則不過濾 Submission
        submissions = None
        if team_id is None:
            submissions = Submission.objects.filter(round__id=round_id)
        else:
            team_id = int(team_id)
            submissions = Submission.objects.filter(team_id=team_id, round__id=round_id)

        # 使用 annotate 來計算每個 Challenge 的最高分
        highest_fitness = (
            submissions.values("challenge")
            .annotate(max_fitness=Max("fitness"))
            .values("challenge", "max_fitness")
        )

        # 將結果整理與輸出
        response = {
            "round_id": round_id,
            "team_id": team_id,
            "total_score": 0,
        }
        for item in highest_fitness:
            print(item)
            response["total_score"] += item["max_fitness"]

        return Response(response, status=status.HTTP_200_OK)
