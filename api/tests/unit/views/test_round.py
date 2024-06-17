from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.model.round import Round
from api.views.round import RoundListAPIView


class RoundListAPIViewTestCase(TestCase):
    def setup(self):
        # Factory
        self.factory = APIRequestFactory()
        # Route
        self.list_route = reverse("round-list")
        self.retrieve_route = reverse("round-detail", kwargs={"pk": 1})
        # Model
        self.r1 = Round.objects.create(
            start_time="2021-01-01 00:00:00", end_time="2030-01-01 00:00:00"
        )
        self.r2 = Round.objects.create(
            start_time="2010-01-01 00:00:00", end_time="2015-01-01 00:00:00"
        )

    @patch("api.views.round.RoundRepository.getCurrentRound")
    @patch("api.views.round.RoundChallengeSerializer")
    def test_get_round_list(self, mock_serializer, mock_get_current_round):
        mock_serializer.return_value.data = {
            "id": 1,
            "start_time": "2021-01-01 00:00:00",
            "end_time": "2030-01-01 00:00:00",
            "challenge_list": [],
        }
        mock_get_current_round.return_value = self.r1

        request = self.factory.get(reverse("round-list"))
        response = RoundListAPIView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OKs)


class RoundAPIViewTestCase(TestCase):
    def setup(self):
        self.factory = APIRequestFactory()

    def test_get_round(self):
        request = self.factory.get(reverse("round-detail", kwargs={"pk": 1}))
        response = RoundListAPIView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
