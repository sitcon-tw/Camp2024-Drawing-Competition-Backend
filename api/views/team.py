import logging

from api.models import Team
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers.team import (
    TeamGeneralSerializer,
    TeamAuthSerializer,
    TeamListSerializer,
)

class TeamAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="List Teams",
        operation_description="List all teams",
        tags=["team"],
        responses={200: TeamListSerializer(many=True)},
    )
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamListSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeamTokenAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Get Team",
        operation_description="Get team by token",
        tags=["team"],
        manual_parameters=[
            openapi.Parameter(
                "token",
                openapi.IN_PATH,
                description="The token of the team",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request,token:str):
        if token:
            team = Team.objects.filter(token=token).first()
            if team:
                return Response(TeamGeneralSerializer(team).data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)


class TeamAuthAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Auth team",
        operation_description="Auth team with token",
        tags=["team"],
        request_body=TeamAuthSerializer,
        responses={200: TeamGeneralSerializer(many=False)},
    )
    def post(self, request):
        data = request.data
        serializer = TeamAuthSerializer(data=data)
        team = Team.objects.filter(name=data["name"], token=data["token"]).first()
        if team:
            return Response(
                {"status": True, "team": TeamGeneralSerializer(team).data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"status": False, "team": None}, status=status.HTTP_200_OK)


class TeamAuthAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Auth team",
        operation_description="Auth team with token",
        tags=["team"],
        request_body=TeamAuthSerializer,
    )
    def post(self, request):
        data = request.data
        serializer = TeamAuthSerializer(data=data)
        team = Team.objects.filter(name=data["name"], token=data["token"]).first()
        if team:
            # Generate a new access token
            access_token = AccessToken.for_user(team)
            return Response(
                {
                    "status": True,
                    "team": TeamGeneralSerializer(team).data,
                    "access_token": str(access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": False, "team": None, "access_token": None},
                status=status.HTTP_200_OK,
            )
