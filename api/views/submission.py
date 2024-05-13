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
)

class SubmissionAPIView(APIView):
    @swagger_auto_schema(
        request_body=SubmissionGeneralSerializer,
    )
    def post(self, request): # 上傳程式碼
        # try:
            serializer = SubmissionGeneralSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            now = datetime.datetime.fromisoformat(request.data.get("time").replace("Z", "+00:00"))
            last_submission = Submission.objects.filter(team__id=request.data["team"]).order_by("time").last()
            if last_submission is None:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            diff_time = now.timestamp() - last_submission.time.timestamp()
            if diff_time < 5 :
                return Response({"message": "Submission too fast"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            else:
                # Create Submission
                serializer.save()

                # Judge Answer
                # TODO: Judge Answer
                return Response({'message': 'success',"data":serializer.data}, status=status.HTTP_200_OK)
        # except Exception as e:
            # logging.error(e)
            # return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubmissionTeamAPIView(APIView):
    def get(self, request, team_id:int): # 取得隊伍的所有提交
        submissions = Submission.objects.filter(team=team_id)
        return Response(SubmissionGeneralSerializer(submissions, many=True).data, status=status.HTTP_200_OK)