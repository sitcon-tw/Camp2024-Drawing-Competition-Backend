import datetime
import logging

from django.utils import timezone
from django.utils.timezone import utc
from api.model.submission import Submission
from api.models import Team
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.submission import (
    SubmissionGeneralSerializer,
    SubmissionCreateSerializer,
)

class SubmissionAPIView(APIView):

    @swagger_auto_schema(
        request_body=SubmissionCreateSerializer,
    )
    def post(self, request):  # 上傳程式碼
        serializer = SubmissionCreateSerializer(data=request.data)
        now = datetime.datetime.now()
        serializer.is_valid(raise_exception=True)

        last_submission = (
            Submission.objects.filter(team__id=request.data["team"])
            .order_by("time")
            .last()
        )
        if last_submission is None:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        diff_time = now.timestamp() - last_submission.time.timestamp()
        if diff_time < 5:
            return Response(
                {"message": "Submission too fast"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        else:
            # Create Submission
            serializer.save()

            # Judge Answer
            # TODO: Judge Answer
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )


class SubmissionChallengeTeamAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="List submission by team and challenge",
        operation_description="List submission by team/challenge id",
        manual_parameters=[
            openapi.Parameter(
                "challenge_id",
                openapi.IN_PATH,
                description="The ID of the challenge",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "team_id",
                openapi.IN_PATH,
                description="The ID of the team",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: SubmissionGeneralSerializer},
    )
    def get(self, request, challenge_id: int, team_id: int):
        submissions = Submission.objects.filter(
            challenge__id=challenge_id, team__id=team_id
        ).order_by("-time")
        return Response(
            SubmissionGeneralSerializer(submissions, many=True).data,
            status=status.HTTP_200_OK,
        )


class SubmissionChallengeTeamMaxAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="get highest score submission by team and challenge",
        operation_description="get highest score submission by team/challenge id",
        manual_parameters=[
            openapi.Parameter(
                "challenge_id",
                openapi.IN_PATH,
                description="The ID of the challenge",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "team_id",
                openapi.IN_PATH,
                description="The ID of the team",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: SubmissionGeneralSerializer},
    )
    def get(self, request, challenge_id: int, team_id: int):
        submissions = (
            Submission.objects.filter(challenge__id=challenge_id, team__id=team_id)
            .order_by("-score")
            .first()
        )
        return Response(
            SubmissionGeneralSerializer(submissions).data,
            status=status.HTTP_200_OK,
        )


class SubmissionTeamAPIView(APIView):
    def get(self, request, team_id:int): # 取得隊伍的所有提交
        submissions = Submission.objects.filter(team=team_id)
        return Response(SubmissionGeneralSerializer(submissions, many=True).data, status=status.HTTP_200_OK)
