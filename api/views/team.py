import logging

from api.models import Team
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
    @swagger_auto_schema(
        request_body=TeamGeneralSerializer,
    )
    def post(self, request):
        data = request.data
        serializer = TeamGeneralSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
