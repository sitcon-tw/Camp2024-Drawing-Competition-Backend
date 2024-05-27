from api.model.challenge import Challenge
from api.model.round import Round
from api.model.team import Team
from api.models import Submission
from django.db.models import Case, When, Max, Value, IntegerField
from django.db.models.functions import Coalesce
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.submission import SubmissionGeneralSerializer


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
        highest_score = (
            submissions.values("challenge")
            .annotate(max_score=Max("score"))
            .values("challenge", "max_score")
        )

        # 將結果整理與輸出
        response = []
        for item in highest_score:
            result = {}
            result["challenge"] = item["challenge"]
            result["max_score"] = item["max_score"]
            result["submission"] = SubmissionGeneralSerializer(
                submissions.filter(
                    challenge=item["challenge"], score=item["max_score"]
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
        highest_score = (
            submissions.values("challenge")
            .annotate(max_score=Max("score"))
            .values("challenge", "max_score")
        )

        # 將結果整理與輸出
        response = {
            "round_id": round_id,
            "team_id": team_id,
            "total_score": 0,
        }
        for item in highest_score:
            print(item)
            response["total_score"] += item["max_score"]

        return Response(response, status=status.HTTP_200_OK)


class StatisticAllTeamSingleRoundTotalScoreAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="List all team total score by round_id",
        operation_description="List all team total score by round_id",
    )
    def get(self, request, round_id: int):
        try:
            round = Round.objects.get(pk=round_id, is_valid=True)
            challenges = Challenge.objects.filter(round_id=round)
            data = []
            for team in Team.objects.all():
                d = {
                    "team_id": team.id,
                    "team_name": team.name,
                    "total_score": 0,
                    "score_list": [],
                }

                for challenge in challenges:
                    total_score = 0
                    highest_score = (
                        Submission.objects.filter(
                            round=round, team=team, challenge=challenge
                        )
                        .values("challenge")
                        .annotate(max_score=Max("score"))
                        .values("challenge", "max_score")
                    )
                    if highest_score:
                        for item in highest_score:
                            total_score += item["max_score"]
                            d["score_list"].append(item["max_score"])
                    else:
                        d["score_list"].append(0)
                d["total_score"] = total_score
                data.append(d)

            return Response(data, status=status.HTTP_200_OK)
        except Round.DoesNotExist:
            return Response(
                {"error": "Round not found"}, status=status.HTTP_404_NOT_FOUND
            )


class StatisticAllTeamRoundTotalScoreAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="List all team total score in every round",
        operation_description="List all team total score in every round",
    )
    def get(self, request):
        submissions = Submission.objects.all()
        data = []
        for team in Team.objects.all():
            d = {
                "team_id": team.id,
                "team_name": team.name,
                "round_id_list": [],
                "total_score_list": [],
            }
            for round in Round.objects.filter(is_valid=True):
                total_score = 0
                highest_score = (
                    submissions.filter(round=round, team=team)
                    .values("challenge")
                    .annotate(max_score=Max("score"))
                    .values("challenge", "max_score")
                )
                for item in highest_score:
                    total_score += item["max_score"]
                d["round_id_list"].append(round.id)
                d["total_score_list"].append(total_score)
            data.append(d)

        return Response(data, status=status.HTTP_200_OK)


class StatisticTop3TeamChallengeScore(APIView):
    def get(self, request, challenge_id: int):
        submissions = Submission.objects.filter(challenge_id=challenge_id)
        # 使用 annotate 來計算每個 Team 的最高分
        highest_score = (
            submissions.values("team")
            .annotate(max_score=Max("score"))
            .values("team", "fitness", "execute_time", "max_score")
            .order_by("-max_score")
        )
        # 將結果整理與輸出
        response = []
        teamList = []
        for item in highest_score:
            if item["team"] in teamList:
                continue
            if len(response) == 3:
                break
            result = {}
            result["team"] = item["team"]
            result["team_name"] = Team.objects.get(id=item["team"]).name
            result["max_score"] = item["max_score"]
            result["fitness"] = item["fitness"]
            result["execute_time"] = item["execute_time"]

            # result["submission"] = SubmissionGeneralSerializer(
            #     submissions.filter(team=item["team"], score=item["max_score"]).first()
            # ).data
            response.append(result)
            teamList.append(item["team"])
        return Response(response, status=status.HTTP_200_OK)
