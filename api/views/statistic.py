from api.model.challenge import Challenge
from api.model.round import Round
from api.model.team import Team
from api.models import Submission
from api.repositories.submission import SubmissionRepository
from api.repositories.challenge import ChallengeRepository
from api.repositories.team import TeamRepository
from api.repositories.round import RoundRepository
from django.db.models import Max
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.submission import SubmissionGeneralSerializer
from api.serializers.statistic import (
    StatisticTeamChallengeScoreResponseDTO,
    StatisticTeamChallengeSubmissionCountResponseDTO,
    StatisticTeamRoundTotalScoreResponseDTO,
    StatisticAllTeamSingleRoundTotalScoreResponseDTO,
    StatisticAllTeamRoundTotalScoreResponseDTO,
    StatisticTop3TeamChallengeScoreResponseDTO,
)

# Infra Repositories
submissionRepository: SubmissionRepository = SubmissionRepository(Submission)
challengeRepository: ChallengeRepository = ChallengeRepository(Challenge)
teamRepository: TeamRepository = TeamRepository(Team)
roundRepository: RoundRepository = RoundRepository(Round)

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
        responses={200: StatisticTeamChallengeScoreResponseDTO(many=True)},
    )
    def get(self, request):
        team_id = request.query_params.get("team_id", None)
        # 如果 team_id 沒有被提供，則不過濾 Submission
        submissions = submissionRepository.findAllSubmissionQueryByTeamId(
            team_id=team_id
        )

        # 使用 annotate 來計算每個 Challenge 的最高分
        highest_score = submissionRepository.getSubmissionHightestScore(submissions)

        # 將結果整理與輸出
        response = []
        for item in highest_score:
            result = {}
            result["challenge"] = item["challenge"]
            result["max_score"] = item["max_score"]
            result["submission"] = SubmissionGeneralSerializer(
                submissionRepository.filterSubmissionByChallengeAndScore(
                    submissions=submissions,
                    challenge=item["challenge"],
                    score=item["max_score"],
                )
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
        responses={200: StatisticTeamChallengeSubmissionCountResponseDTO(many=True)},
    )
    def get(self, request):
        team_id = request.query_params.get("team_id", None)
        # 如果 team_id 沒有被提供，則不過濾 Submission
        submissions = submissionRepository.findAllSubmissionQueryByTeamId(
            team_id=team_id
        )

        result = []
        for challenge in challengeRepository.find_all():
            submission_count = (
                submissionRepository.countSubmissionQueryByTeamIdFilterByChallenge(
                    submissions=submissions, team_id=team_id, challenge=challenge
                )
            )
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
        responses={200: StatisticTeamRoundTotalScoreResponseDTO(many=False)},
    )
    def get(self, request, round_id: int):
        team_id = request.query_params.get("team_id", None)
        # 如果 team_id 沒有被提供，則不過濾 Submission
        submissions = submissionRepository.findAllSubmissionQueryByTeamId(
            team_id=team_id
        )
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
            response["total_score"] += item["max_score"]

        return Response(response, status=status.HTTP_200_OK)


class StatisticAllTeamSingleRoundTotalScoreAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="List all team total score by round_id",
        operation_description="List all team total score by round_id",
        responses={200: StatisticAllTeamSingleRoundTotalScoreResponseDTO(many=True)},
    )
    def get(self, request, round_id: int):
        try:
            round_instance = Round.objects.get(pk=round_id, is_valid=True)
            challenges = Challenge.objects.filter(round_id=round_instance)
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
                            round=round_instance, team=team, challenge=challenge
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
        responses={200: StatisticAllTeamRoundTotalScoreResponseDTO(many=True)},
    )
    def get(self, request):
        submissions = submissionRepository.find_all()
        data = []
        for team in teamRepository.find_all():
            d = {
                "team_id": team.id,
                "team_name": team.name,
                "round_id_list": [],
                "total_score_list": [],
            }
            for round_instance in roundRepository.findAllValidRound():
                total_score = 0
                highest_score = (
                    submissionRepository.getSubmissionHightestScoreByRoundAndTeam(
                        submissions=submissions, round=round_instance, team=team
                    )
                )
                for item in highest_score:
                    total_score += item["max_score"]
                d["round_id_list"].append(round_instance.id)
                d["total_score_list"].append(total_score)
            data.append(d)

        return Response(data, status=status.HTTP_200_OK)


class StatisticTop3TeamChallengeScore(APIView):

    @swagger_auto_schema(
        operation_summary="List top3 team score in challenge",
        operation_description="List top3 team score in challenge",
        manual_parameters=[
            openapi.Parameter(
                "challenge_id",
                openapi.IN_PATH,
                description="The ID of the challenge",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: StatisticTop3TeamChallengeScoreResponseDTO(many=True)},
    )
    def get(self, request, challenge_id: int):
        submissions = submissionRepository.findAllSubmissionByChallengeId(
            challenge_id=challenge_id
        )
        # 使用 annotate 來計算每個 Team 的最高分
        highest_score = submissionRepository.getSubmissionHightestScoreWithFullRecord(
            submissions
        )
        # 將結果整理與輸出
        response = []
        team_list = []
        for item in highest_score:
            if item["team"] in team_list:
                continue
            if len(response) == 3:
                break
            result = {}
            result["team"] = item["team"]
            result["team_name"] = teamRepository.get_by_id(item["team"]).name
            result["max_score"] = item["max_score"]
            result["fitness"] = item["fitness"]
            result["execute_time"] = item["execute_time"]

            response.append(result)
            team_list.append(item["team"])
        return Response(response, status=status.HTTP_200_OK)
