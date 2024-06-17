from api.repositories.base import Repository
from django.utils import timezone


class RoundRepository(Repository):
    # 取得當前 Round
    def getCurrentRound(self):
        return self.class1.objects.filter(
            start_time__lte=timezone.now(), end_time__gte=timezone.now()
        ).last()

    # 檢查是否含有有效的 Round
    def checkValidRoundExists(self):
        return self.class1.objects.filter(is_valid=True).exists()

    # 取得所有有效的 Round
    def findAllValidRound(self):
        return self.class1.objects.filter(is_valid=True)
