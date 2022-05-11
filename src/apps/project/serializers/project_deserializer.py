import datetime
from apps.project.models import Organization
from apps.project.models.file import ProjectFile

class ProjectDeserializer:

    def __init__(self, project):
        self.project = project
    
    def from_dict(self, data):

        self.project.direction_id = data["direction_id"]
        self.project.subject_id = data["subject_id"]
        self.project.title = data["title"]
        self.project.description = data["description"]
        self.project.geography = data["geography"]
        if data["start_date"]:
            self.project.start_date = datetime.datetime.strptime(
                data["start_date"], '%Y-%m-%d')

        if data["finish_date"]:
            self.project.finish_date = datetime.datetime.strptime(
                data["finish_date"], '%Y-%m-%d')
        self.project.social_significance = data["social_significance"]
        self.project.info_support = data["info_support"]
        self.project.quality_results = data["quality_results"]
        self.project.further_progress = data["further_progress"]
        self.project.sources = data["sources"]

        self.project.manager.position = data["manager"]["position"]
        self.project.manager.last_name = data["manager"]["last_name"]
        self.project.manager.first_name = data["manager"]["first_name"]
        self.project.manager.middle_name = data["manager"]["middle_name"]
        self.project.manager.degree = data["manager"]["degree"]
        self.project.manager.work_phone = data["manager"]["work_phone"]
        self.project.manager.mobile_phone = data["manager"]["mobile_phone"]
        self.project.manager.email = data["manager"]["email"]
        self.project.manager.education = data["manager"]["education"]
        self.project.manager.info = data["manager"]["info"]
        self.project.manager.social_links = data["manager"]["social_links"]
        self.project.manager.academic_rank = data["manager"]["academic_rank"]
        
        if data["manager"]["birth_date"]:
            self.project.manager.birth_date = datetime.datetime.strptime(data["manager"]["birth_date"], '%Y-%m-%d')

        if self.project.organization is None:
            self.project.organization_id = Organization.objects.create().id
        self.project.organization.ogrn = data["organization"]["ogrn"]
        self.project.organization.inn = data["organization"]["inn"]
        self.project.organization.kpp = data["organization"]["kpp"]
        self.project.organization.full_name = data["organization"]["full_name"]
        self.project.organization.short_name = data["organization"]["short_name"]

        if data["organization"]["registration_date"]:
            self.project.organization.registration_date = datetime.datetime.strptime(data["organization"]["registration_date"], '%Y-%m-%dT%H:%M:%S.000Z')

        self.project.organization.address = data["organization"]["address"]
        self.project.organization.fact_address = data["organization"]["fact_address"]
        self.project.organization.legal_address = data["organization"]["legal_address"]
        self.project.organization.main_activities = data["organization"]["main_activities"]
        self.project.organization.phone = data["organization"]["phone"]
        self.project.organization.legal_email = data["organization"]["legal_email"]
        self.project.organization.email = data["organization"]["email"]
        self.project.organization.web = data["organization"]["web"]
        self.project.organization.social = data["organization"]["social"]
        self.project.organization.manager_fio = data["organization"]["manager_fio"]
        self.project.organization.manager_correct = data["organization"]["manager_correct"]
        self.project.organization.manager_position = data["organization"]["manager_position"]
        self.project.organization.short_name = data["organization"]["short_name"]
        if data["organization"]["manager_birth_date"]:
            self.project.organization.manager_birth_date = datetime.datetime.strptime(data["organization"]["manager_birth_date"], '%Y-%m-%dT%H:%M:%S.000Z')

        self.project.organization.trusted_persons = data["organization"]["trusted_persons"]
        self.project.organization.collegial_managers = data["organization"]["collegial_managers"]
        self.project.organization.accountant = data["organization"]["accountant"]
        self.project.organization.foreign_founders = data["organization"]["foreign_founders"]
        self.project.organization.legal_founders = data["organization"]["legal_founders"]
        self.project.organization.structural_units = data["organization"]["structural_units"]
        self.project.organization.non_commercial_organizations = data["organization"]["non_commercial_organizations"]
        self.project.organization.commercial_organizations = data["organization"]["commercial_organizations"]
        self.project.organization.members_count = data["organization"]["members_count"]

        self.project.organization.employees_count = data["organization"]["employees_count"]
        self.project.organization.volunteers_count = data["organization"]["volunteers_count"]
        self.project.organization.presidential_grants = data["organization"]["presidential_grants"]
        self.project.organization.non_commercial_grants = data["organization"]["non_commercial_grants"]
        self.project.organization.commercial_grants = data["organization"]["commercial_grants"]
        self.project.organization.membership_fee = data["organization"]["membership_fee"]
        self.project.organization.foreign_grants = data["organization"]["foreign_grants"]
        self.project.organization.federal_budget = data["organization"]["federal_budget"]
        self.project.organization.region_budget = data["organization"]["region_budget"]
        self.project.organization.local_budget = data["organization"]["local_budget"]
        self.project.organization.revenue = data["organization"]["revenue"]
        self.project.organization.dividends = data["organization"]["dividends"]
        self.project.organization.other_income = data["organization"]["other_income"]
        self.project.organization.total_cost = data["organization"]["total_cost"]
        self.project.organization.media_publications = data["organization"]["media_publications"]
        self.project.organization.success_projects = data["organization"]["success_projects"]
        self.project.organization.beneficiaries_count = data["organization"]["beneficiaries_count"]
        self.project.organization.material_resources = data["organization"]["material_resources"]
        self.project.organization.support_type = data["organization"]["support_type"]

        files = [x for x in data['project_files'] if not 'id' in x and 'url' in x] 
        for file in files:
            url = file['url']
            is_standart = str.startswith(url, '/media/contur/')
            if is_standart:
                if file['type'] == 'organization_egrul':
                    file_url = str.replace(url,'/media/', '')
                    if not ProjectFile.objects.all().filter(project=self.project, type=ProjectFile.TYPE_ORGANIZATION_EGRUL, file=file_url):
                        pf = ProjectFile()
                        pf.type = pf.TYPE_ORGANIZATION_EGRUL
                        pf.project = self.project
                        pf.file = file_url
                        pf.save()

                pass


        return self.project