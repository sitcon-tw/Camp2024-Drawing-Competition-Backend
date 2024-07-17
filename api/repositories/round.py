from api.repositories.base import Repository
from django.utils import timezone
from django.utils.timezone import datetime

class RoundRepository(Repository):
    # 取得當前 Round
    def getCurrentRound(self):
        
        print(f"==={datetime.now()} {timezone.localtime()} {timezone.now()}===")

        matching_rounds = self.class1.objects.filter(
            start_time__lte=timezone.localtime(),
            end_time__gte=timezone.localtime(),
        )
        if not matching_rounds:
            return None
        round = matching_rounds.first()
        print(round.start_time)
        return round
    
    # 檢查是否含有有效的 Round
    def checkValidRoundExists(self):
        return self.class1.objects.filter(is_valid=True).exists()

    # 取得所有有效的 Round
    def findAllValidRound(self):
        return self.class1.objects.filter(is_valid=True)
