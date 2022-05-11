import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from apps.project.models import Project, Goal, Job, ProjectManager, ProjectMember, Event, GenericCost, TargetGroup, \
    Organization, Partner, Institution, Report, QuantResult, Geography
from apps.project.serializers import InstitutionDeserializer, QuantResultDeserializer, GeographyDeserializer
from apps.project.serializers import JobDeserializer, GoalDeserializer, TargetGroupDeserializer, PartnerDeserializer
from apps.project.serializers import ProjectDeserializer, ProjectMemberDeserializer, EventDeserializer, \
    GenericCostDeserializer


def create_empty_project(data):
    manager = ProjectManager.objects.create()
    organization = Organization.objects.create()
    project = Project()
    project.status = Project.DRAFT
    project.contest_id = data["contest_id"]
    project.author_id = data["user_id"]
    project.manager_id = manager.id
    project.organization_id = organization.id
    project.save()

    Goal.objects.create(project_id=project.id)
    Job.objects.create(project_id=project.id)
    ProjectMember.objects.create(project_id=project.id)
    QuantResult.objects.create(project_id=project.id, guid=uuid.uuid4(), name='Количество благополучателей', count=0)

    return project


def update_project(project, data):
    project = ProjectDeserializer(project).from_dict(data)
    project.save()
    project.manager.save()
    project.organization.save()

    update_project_relation(Goal, GoalDeserializer, project.id, data["goals"])
    update_project_relation(
        TargetGroup, TargetGroupDeserializer, project.id, data["target_groups"])
    update_project_relation(Job, JobDeserializer, project.id, data["jobs"])
    update_project_relation(Partner, PartnerDeserializer,
                            project.id, data["partners"])
    update_project_relation(
        ProjectMember, ProjectMemberDeserializer, project.id, data["members"])
    update_project_relation(Event, EventDeserializer,
                            project.id, data["events"])
    update_project_relation(
        GenericCost, GenericCostDeserializer, project.id, data["generic_costs"])

    update_project_relation(
        Institution, InstitutionDeserializer, project.id, data["institutions"])

    update_project_relation(
        QuantResult, QuantResultDeserializer, project.id, data["quant_results"])

    update_project_relation(
        Geography, GeographyDeserializer, project.id, data["geography"])

    return project


def update_project_relation(RelClass, DeserClass, project_id, items):
    for item in items:
        if item["status"] == "delete" and "id" in item:
            try:
                obj = RelClass.objects.get(pk=item["id"])
                obj.delete()
            except ObjectDoesNotExist:
                pass
            continue
        elif item["status"] == "delete":
            continue

        if item["status"] == "update" and "id" in item:
            obj = RelClass.objects.get(pk=item["id"])
        else:
            obj = RelClass(project_id=project_id)

        DeserClass(obj).from_dict(item).save()


def remove_project(project):
    project.manager.delete()
    return project.delete()


def get_user_projects(user_id):
    return Project.objects.all().filter(author=user_id)


def get_expert_projects(user_id):
    return Project.objects.all().filter(experts=user_id)


def get_project(id):
    return get_object_or_404(Project, pk=id)


def get_project_report(project_id):
    project = get_object_or_404(Project, pk=project_id)

    try:
        report = project.report
    except ObjectDoesNotExist:
        report = Report.objects.create(project=project, status=Report.DRAFT)

    return report
