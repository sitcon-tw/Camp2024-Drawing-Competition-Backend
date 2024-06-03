from api.repositories.base import Repository
from django.db.models import Max
from api.models import Submission, Challenge, Round, Team
from django.db.models.manager import BaseManager


class SubmissionRepository(Repository):
    # 取得最新一筆 Submission
    def getLastSubmission(self):
        return self.class1.objects.last()

    # 取得該 Team 最新一筆 Submission
    def findNewestSubmissionByTeamId(self, teamId: int):
        return self.class1.objects.filter(team__id=teamId).order_by("time").last()

    # 取得該 Team Challenge 依照時間排序的 Submission
    def findAllSubmissionByChallengeIdAndTeamId(self, challengeId: int, teamId: int):
        return self.class1.objects.filter(
            challenge__id=challengeId, team__id=teamId
        ).order_by("-time")

    # 取得該 Team Challenge 最高分 Submission
    def findMaxScoreSubmissionByChallengeIdAndTeamId(
        self, challengeId: int, teamId: int
    ):
        return (
            self.class1.objects.filter(challenge__id=challengeId, team__id=teamId)
            .order_by("-score")
            .first()
        )

    # 取得該 Challenge 所有 Submission
    def findAllSubmissionByChallengeId(self, challengeId: int):
        return self.class1.objects.filter(challenge__id=challengeId)

    # 取得該 Team 所有 Submission
    def findAllSubmissionByTeamId(self, teamId: int):
        return self.class1.objects.filter(team__id=teamId)

    # 根據是否有 TeamId 取得所有 Submission 並依照 Challenge 和 反向 time 排序
    def findAllSubmissionQueryByTeamIdOrderByChallengeAndReverseTime(self, teamId: int):
        if teamId is None:
            latest_submissions = self.class1.objects.all().order_by(
                "challenge", "-time"
            )
        else:
            latest_submissions = self.class1.objects.filter(team__id=teamId).order_by(
                "challenge", "-time"
            )
        return latest_submissions

    # 過濾 Submission 根據 Challenge 最新一筆 Submission
    def filterSubmissionByChallenge(
        self, submissions: BaseManager[Submission], challenge: Challenge
    ):
        return submissions.filter(challenge=challenge).first()

    # 根據 TeamId 取得所有 Submission
    def findAllSubmissionQueryByTeamId(self, teamId: int):
        if teamId is None:
            return self.class1.objects.all()
        else:
            return self.class1.objects.filter(team__id=teamId)

    # 過濾當前 submission 取出各 Challenge 最高分
    def getSubmissionHightestScore(self, submissions: BaseManager[Submission]):
        return (
            submissions.values("challenge")
            .annotate(max_score=Max("score"))
            .values("challenge", "max_score")
        )

    # 過濾當前 submission 根據 Round 與 Team 取出各 Challenge 最高分
    def getSubmissionHightestScoreByRoundAndTeam(
        self, submissions: BaseManager[Submission], round: Round, team: Team
    ):
        return (
            submissions.filter(round=round, team=team)
            .values("challenge")
            .annotate(max_score=Max("score"))
            .values("challenge", "max_score")
        )

    # 過濾當前 submission 取出各 Challenge 最高分並給予 Team 吻合度 執行時間 與最高分
    def getSubmissionHightestScoreWithFullRecord(
        self, submissions: BaseManager[Submission]
    ):
        return (
            submissions.values("team")
            .annotate(max_score=Max("score"))
            .values("team", "fitness", "execute_time", "max_score")
            .order_by("-max_score")
        )

    # 過濾 Submission 根據 Challenge 與 Score 取出 Submission
    def filterSubmissionByChallengeAndScore(
        self, submissions: BaseManager[Submission], challenge, score
    ):
        return submissions.filter(challenge=challenge, score=score).first()

    # 計算 Submission 個數根據 TeamId 與 Challenge
    def countSubmissionQueryByTeamIdFilterByChallenge(
        self, submissions: BaseManager[Submission], teamId: int, challenge: Challenge
    ):
        submission_count = 0
        if teamId is None:
            submission_count = submissions.filter(challenge=challenge).count()
        else:
            submission_count = submissions.filter(
                challenge=challenge, team_id=teamId
            ).count()
        return submission_count

    # 取得 Submission 根據 TeamId 與 RoundId
    def findAllSubmissionQueryByTeamIdAndFilterByRoundId(
        self, teamId: int, roundId: int
    ):
        if team_id is None:
            submissions = Submission.objects.filter(round__id=roundId)
        else:
            team_id = int(teamId)
            submissions = Submission.objects.filter(team_id=teamId, round__id=roundId)
        return submissions
