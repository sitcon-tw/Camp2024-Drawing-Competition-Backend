from api.model.round import Round
from api.repositories.base import Repository
from api.repositories.round import RoundRepository

roundRepository: RoundRepository = RoundRepository(Round)

class ChallengeRepository(Repository):

    def find_by_id_with_round(self, pk: int):
        return self.class1.objects.filter(
            pk=pk, round_id=roundRepository.getCurrentRound()
        ).first()
