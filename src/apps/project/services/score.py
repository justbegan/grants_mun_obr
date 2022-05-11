from apps.contest.models import ScoreSheet, Score, Coefficient
from apps.project.services.project import get_project
from datetime import date, datetime


def get_score_sheet(project_id, expert_id):
    project = get_project(project_id)
    score_sheets = ScoreSheet.objects.all().filter(
        project_id=project_id, author_id=expert_id)

    if score_sheets:
        score_sheet = score_sheets[0]

        if project.organization.support_type == project.organization.TYPE_1:
            score_sheet.additional_score1 = 5
        init_scores(project, score_sheet)

        return score_sheet

    score_sheet = ScoreSheet(
        project_id=project_id, contest_id=project.contest_id, author_id=expert_id)

    if project.organization.support_type == project.organization.TYPE_1:
        score_sheet.additional_score1 = 0 # Пока отключил автоматическое выставление балла (было 5)
    else:
        score_sheet.additional_score1 = 0
    score_sheet.updated_on = datetime.now() # check включил из-зи exception
    score_sheet.save()

    init_scores(project, score_sheet)

    return score_sheet


def init_scores(project, score_sheet):
    for coefficient in Coefficient.objects.all().filter(contest_id=project.contest_id):
        not_found = True
        for score in score_sheet.score_set.all():
            if score.criteria_id == coefficient.criteria_id:
                not_found = False

        if not_found:
            new_score = Score()
            new_score.score_sheet_id = score_sheet.id
            new_score.criteria_id = coefficient.criteria_id
            new_score.score = 0
            new_score.updated_on = datetime.now() # check включил из-зи exception
            new_score.save()


def get_score_sheets(expert_id):
    return ScoreSheet.objects.all().filter(author_id=expert_id)
