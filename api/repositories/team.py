from api.repositories.base import Repository


class TeamRepository(Repository):
    # 根據 Token 取得 Team
    def getTeamByToken(self, token):
        return self.class1.objects.filter(token=token).first()
