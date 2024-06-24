from api.model.submission import Submission
from api.models import Challenge
from api.repositories.challenge import ChallengeRepository
from api.repositories.submission import SubmissionRepository
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from api.serializers.challenge import (
    ChallengeGeneralSerializer,
    ChallengeTeamSubmissionSerializer,
)
# Infra Repositories
repository: ChallengeRepository = ChallengeRepository(Challenge)
submissionRepository: SubmissionRepository = SubmissionRepository(Submission)


class ChallengeAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get all challenges",
        operation_description="Get all challenges",
        responses={200: ChallengeGeneralSerializer(many=True)},
    )
    def get(self, request):
        challenges = repository.find_all()
        return Response(
            ChallengeGeneralSerializer(challenges, many=True).data,
            status=status.HTTP_200_OK,
        )


class ChallengeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ChallengeGeneralSerializer
    queryset = repository.find_all()


class ChallengeRetrieveSingleAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Get challenge by id",
        operation_description="Get Challenge by id",
        responses={200: ChallengeTeamSubmissionSerializer(many=False)},
    )
    def get(self, request, id: int):
        challenge = repository.find_by_id_with_round(pk=id)
        if challenge:
            return Response(
                ChallengeGeneralSerializer(challenge).data, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Challenge is not valid"}, status=status.HTTP_400_BAD_REQUEST
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
        responses={200: ChallengeTeamSubmissionSerializer(many=True)},
    )
    def get(self, request):
        team_id = request.GET.get("team_id", None)
        challenges = repository.find_all()
        latest_submissions = submissionRepository.findAllSubmissionByTeamId(team_id)

        challenge_status_list = []
        for challenge in challenges:
            challenge_status = submissionRepository.filterSubmissionByChallenge(
                latest_submissions, challenge
            )
            c_status = "todo"
            if challenge_status is not None:
                c_status = challenge_status.status
            challenge_status_list.append(c_status)

        team_challenges = []
        for challenge, c_status in zip(challenges, challenge_status_list):
            d = {}
            d["id"] = challenge.id
            d["title"] = challenge.title
            d["description"] = challenge.description
            d["round_id"] = challenge.round_id.id
            d["is_valid"] = challenge.is_valid
            d["difficulty"] = challenge.difficulty
            d["status"] = c_status
            team_challenges.append(d)
        return Response(
            ChallengeTeamSubmissionSerializer(team_challenges, many=True).data,
            status=status.HTTP_200_OK,
        )
