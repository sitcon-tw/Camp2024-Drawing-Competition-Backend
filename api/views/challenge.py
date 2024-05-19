from api.model.submission import Submission
from api.models import Challenge
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from api.serializers.challenge import (
    ChallengeGeneralSerializer,
    ChallengeTeamSubmissionSerializer,
)


class ChallengeAPIView(APIView):
    # parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Get all challenges",
        operation_description="Get all challenges",
        responses={200: ChallengeGeneralSerializer(many=True)},
    )
    def get(self, request):
        challenges = Challenge.objects.all()
        return Response(
            ChallengeGeneralSerializer(challenges, many=True).data,
            status=status.HTTP_200_OK,
        )


class ChallengeRUDAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get challenge by ID",
        operation_description="Get challenge by ID",
        manual_parameters=[
            openapi.Parameter(
                "challenge_id",
                openapi.IN_PATH,
                description="The ID of the challenge",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: ChallengeGeneralSerializer},
    )
    def get(self, request, challenge_id: int):
        challenge = Challenge.objects.get(id=challenge_id)
        return Response(
            ChallengeGeneralSerializer(challenge).data,
            status=status.HTTP_200_OK,
        )


class ChallengeTeamListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="List challenge by team",
        operation_description="List Challenge by team",
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
        team_id = request.GET.get("team_id", None)
        challenges = Challenge.objects.all()
        latest_submissions = None
        if team_id is None:
            latest_submissions = Submission.objects.all().order_by("challenge", "-time")
        else:
            latest_submissions = Submission.objects.filter(team__id=team_id).order_by(
                "challenge", "-time"
            )
        challenge_status_list = []
        for challenge in challenges:
            challenge_status = latest_submissions.filter(challenge=challenge).first()
            c_status = "todo"
            if challenge_status is not None:
                c_status = challenge_status.status
            challenge_status_list.append(c_status)

        team_challenges = []
        for challenge, c_status in zip(challenges, challenge_status_list):
            d = {}
            d["id"] = challenge.id
            d["description"] = challenge.description
            d["round_id"] = challenge.round_id.id
            d["is_valid"] = challenge.is_valid
            d["status"] = c_status
            team_challenges.append(d)
        return Response(
            ChallengeTeamSubmissionSerializer(team_challenges, many=True).data,
            status=status.HTTP_200_OK,
        )
