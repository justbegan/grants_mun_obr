import json
from apps.project.services.checklist import OrganizationValidate


class ProjectSerializer:

    def __init__(self, project):
        self.project = project

    def to_json(self):
        # Цели проекта
        goals = []
        for goal in self.project.goal_set.all():
            goals.append({
                "id": goal.id,
                "content": goal.content,
                "guid": goal.guid,
                "status": "update",
            })

        # Целевые группы
        target_groups = []
        for target_group in self.project.targetgroup_set.all():
            target_groups.append({
                "id": target_group.id,
                "content": target_group.title,
                "guid": target_group.guid,
                "status": "update",
                "type": target_group.type
            })

        # Задачи проекта
        jobs = []
        for job in self.project.job_set.all():
            jobs.append({
                "id": job.id,
                "content": job.content,
                "guid": job.guid,
                "status": "update",
            })

        # Партнеры проекта
        partners = []
        for partner in self.project.partner_set.all():
            supports = []
            if partner.supports:
                for support in partner.supports.split(','):
                    supports.append({
                        "text": support,
                    })
            partners.append({
                "id": partner.id,
                "name": partner.name,
                "guid": partner.guid,
                "supports": supports,
                "status": "update",
            })


        # Команда проекта
        members = []
        for member in self.project.projectmember_set.all():
            members.append({
                "id": member.id,
                "guid": member.guid,
                "status": "update",
                "position": member.position,
                "last_name": member.last_name,
                "first_name": member.first_name,
                "middle_name": member.middle_name,
                "education": member.education,
                "info": member.info,
            })

        # Календарный план
        events = []
        for event in self.project.event_set.all():
            events.append({
                "id": event.id,
                "guid": event.guid,
                "status": "update",
                "job_id": event.job_id,
                "name": event.name,
                "start_date": event.start_date.strftime('%Y-%m-%d') if event.start_date is not None else  '',
                "finish_date": event.finish_date.strftime('%Y-%m-%d') if event.finish_date is not None else  '',
                "result": event.result,
            })

        # Бюджет
        generic_costs = []
        for generic_cost in self.project.genericcost_set.all():
            generic_costs.append({
                "id": generic_cost.id,
                "guid": generic_cost.guid,
                "status": "update",
                "name": generic_cost.name,
                "cost": generic_cost.cost,
                "items_count": generic_cost.items_count,
                "co_financing": generic_cost.co_financing,
                "comment": generic_cost.comment,
                "type": generic_cost.type,
            })

        # Место работы / учебы
        institutions = []
        for institution in self.project.institution_set.all():
            institutions.append({
                "id": institution.id,
                "guid": institution.guid,
                "status": "update",
                "organization": institution.organization,
                "position": institution.position,
                "start_date": institution.start_date.strftime('%Y-%m-%d') if institution.start_date is not None else  '',
                "finish_date": institution.finish_date.strftime('%Y-%m-%d') if institution.finish_date is not None else  '',
                "in_present": institution.in_present,
                "member_id": institution.member_id,
                "manager_id": institution.manager_id,
                "type": institution.type,
            })

        project_files = []
        for project_file in self.project.projectfile_set.all():
            project_files.append({
                "id": project_file.id,
                "status": "update",
                "name": project_file.file,
                "type": project_file.type,
            })

        # Количественные результаты
        quant_results = []
        for result in self.project.quantresult_set.all():
            quant_results.append({
                "id": result.id,
                "guid": result.guid,
                "status": "update",
                "name": result.name,
                "count": result.count,
            })

        # География
        geography_list = []
        for geo in self.project.geography_set.all():
            geography_list.append({
                "id": geo.id,
                "guid": geo.guid,
                "project_id": self.project.id,
                'organization_id': geo.organization_id,
                "status": "update",
                "name": geo.name,
            })

        return json.dumps({
            "id": self.project.id,
            "created_on": self.project.created_on,
            "update_on": self.project.updated_on,
            "direction_id": self.project.direction_id,
            "subject_id": self.project.subject_id,
            "title": self.project.title,
            "description": self.project.description,
            "geography": geography_list,
            "start_date": self.project.start_date.strftime('%Y-%m-%d') if self.project.start_date is not None else '',
            "finish_date": self.project.finish_date.strftime('%Y-%m-%d') if self.project.finish_date is not None else '',
            "social_significance": self.project.social_significance,
            "goals": goals,
            "partners": partners,
            "target_groups": target_groups,
            "jobs": jobs,
            "info_support": self.project.info_support,
            "quant_results": quant_results,
            "quality_results": self.project.quality_results,
            "further_progress": self.project.further_progress,
            "sources": self.project.sources,
            "manager": {
                "id": self.project.manager.id,
                "position": self.project.manager.position,
                "last_name": self.project.manager.last_name,
                "first_name": self.project.manager.first_name,
                "middle_name": self.project.manager.middle_name,
                "degree": self.project.manager.degree,
                "work_phone": self.project.manager.work_phone,
                "mobile_phone": self.project.manager.mobile_phone,
                "email": self.project.manager.email,
                "education": self.project.manager.education,
                "info": self.project.manager.info,
                "birth_date": self.project.manager.birth_date.strftime('%Y-%m-%d') if self.project.manager.birth_date is not None else '',
                "social_links": self.project.manager.social_links,
                "academic_rank": self.project.manager.academic_rank,
            },
            "members": members,
            "organization": {
                "id": self.project.organization.id,
                "ogrn": self.project.organization.ogrn if self.project.organization is not None else '',
                "inn": self.project.organization.inn if self.project.organization is not None else '',
                "kpp": self.project.organization.kpp if self.project.organization is not None else '',
                "full_name": self.project.organization.full_name if self.project.organization is not None else '',
                "short_name": self.project.organization.short_name if self.project.organization is not None else '',
                "registration_date": self.project.organization.registration_date.strftime('%Y-%m-%dT%H:%M:%S.000Z') if self.project.organization.registration_date is not None else '',
                "address": self.project.organization.address,
                "fact_address": self.project.organization.fact_address,
                "legal_address": self.project.organization.legal_address,
                "main_activities": self.project.organization.main_activities,
                "phone": self.project.organization.phone,
                "legal_email": self.project.organization.legal_email,
                "email": self.project.organization.email,
                "web": self.project.organization.web,
                "social": self.project.organization.social,
                "manager_fio": self.project.organization.manager_fio,
                "manager_position": self.project.organization.manager_position,
                "manager_correct": self.project.organization.manager_correct,
                "manager_birth_date": self.project.organization.manager_birth_date.strftime('%Y-%m-%dT%H:%M:%S.000Z') if self.project.organization.manager_birth_date is not None else '',
                
                "trusted_persons": self.project.organization.trusted_persons,
                "collegial_managers": self.project.organization.collegial_managers,
                "accountant": self.project.organization.accountant,
                "foreign_founders": self.project.organization.foreign_founders,
                "legal_founders": self.project.organization.legal_founders,
                "structural_units": self.project.organization.structural_units,
                "non_commercial_organizations": self.project.organization.non_commercial_organizations,
                "commercial_organizations": self.project.organization.commercial_organizations,
                "members_count": self.project.organization.members_count,

                "employees_count": self.project.organization.employees_count,
                "volunteers_count": self.project.organization.volunteers_count,
                "presidential_grants": self.project.organization.presidential_grants,
                "non_commercial_grants": self.project.organization.non_commercial_grants,
                "commercial_grants": self.project.organization.commercial_grants,
                "membership_fee": self.project.organization.membership_fee,
                "foreign_grants": self.project.organization.foreign_grants,
                "federal_budget": self.project.organization.federal_budget,
                "region_budget": self.project.organization.region_budget,
                "local_budget": self.project.organization.local_budget,
                "revenue": self.project.organization.revenue,
                "dividends": self.project.organization.dividends,
                "other_income": self.project.organization.other_income,
                "total_cost": self.project.organization.total_cost,
                "beneficiaries_count": self.project.organization.beneficiaries_count,
                "media_publications": self.project.organization.media_publications,
                "success_projects": self.project.organization.success_projects,
                "material_resources": self.project.organization.material_resources,
                "support_type": self.project.organization.support_type,
                "checklist": OrganizationValidate(self.project.organization, None).toJSON()
            },
            "events": events,
            "generic_costs": generic_costs,
            "project_files": project_files,
            "institutions": institutions,

        }, indent=2, default=str)
