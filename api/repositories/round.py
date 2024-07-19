from api.repositories.base import Repository
from django.utils import timezone
from django.utils.timezone import datetime

class RoundRepository(Repository):
    # 取得當前 Round
    def getCurrentRound(self):
        
        print(f"==={datetime.now()} {timezone.localtime()}===")
        print(self.class1.objects.all().first().start_time)
        return self.class1.objects.filter(
            start_time__lte=timezone.localtime(),end_time__gte=timezone.localtime()
        ).first()
    
    # 檢查是否含有有效的 Round
    def checkValidRoundExists(self):
        print(">>>",self.class1.objects.filter(is_valid=False).exists())
        return self.class1.objects.filter(is_valid=False).exists()

    # 取得所有有效的 Round
    def findAllValidRound(self):
        return self.class1.objects.filter(is_valid=True)
