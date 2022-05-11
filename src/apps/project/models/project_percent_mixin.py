from django.db.models.query import QuerySet


class ProjectPercentMixin:
    """ Процент заполненности проекта """

    """ О проекте """
    def about_percent(self):
        fields = {
            'direction', 'title', 'description', 'start_date', 'geography_set',
            'finish_date', 'social_significance', 'info_support',
            'targetgroup_set', 'goal_set', 'job_set','partner_set',
            'info_support', 'quantresult_set', 'quality_results', 'further_progress', 'sources'
        }

        return self.percent(self, fields, self, 'project')

    """ Руководитель """
    def manager_percent(self):
        fields = {
            'position', 'last_name', 'first_name', 'middle_name',
            'education',  'work_phone', 'mobile_phone', 'email',
            'education_set', 'work_set', 'birth_date',
        }

        return self.percent(self.manager, fields)

    """ Команда """
    def members_percent(self):
        fields = {'position', 'last_name', 'first_name', 'middle_name', 'education',}
        count = 0
        percent_sum = 0
        for member in self.projectmember_set.all():
            percent_sum = percent_sum + self.percent(member, fields)
            count = count + 1

        if count == 0:
            return 0

        return round(percent_sum / count)

    """ Организация """
    def organization_percent(self):
        from apps.project.models import ProjectFile
        fields = {
            'ogrn', 'inn', 'kpp', 'full_name', 'short_name', 'registration_date',
            'address', 'legal_address', 'main_activities', 
            'geography_set', 'phone', 'legal_email', 'manager_fio',
            'manager_position', 'trusted_persons','material_resources',
            ProjectFile.TYPE_ORGANIZATION_EGRUL,
            ProjectFile.TYPE_ORGANIZATION_USTAV
          }

        return self.percent(self.organization, fields, self, 'organization')

    @staticmethod
    def percent(obj, fields, project=None, section='project'):
        from apps.project.models import ProjectFile
        """Процент заполненности полей"""
        count = 0
        for attrName in fields:
            k = 0
            if attrName == 'geography_set' and section == 'project':
                files = project.geography_set.all().filter(organization__isnull=True)
                if len(files) > 0:
                    k = 1
                else:
                    k = 0
            elif attrName == ProjectFile.TYPE_ORGANIZATION_EGRUL:
                files = project.projectfile_set.all().filter(type=ProjectFile.TYPE_ORGANIZATION_EGRUL)
                if len(files) > 0:
                    k = 1
                else:
                    k = 0
            elif attrName == ProjectFile.TYPE_ORGANIZATION_NALOG:
                files = project.projectfile_set.all().filter(type=ProjectFile.TYPE_ORGANIZATION_NALOG)
                if len(files) > 0:
                    k = 1
                else:
                    k = 0
            elif attrName == ProjectFile.TYPE_ORGANIZATION_SOGR:
                files = project.projectfile_set.all().filter(type=ProjectFile.TYPE_ORGANIZATION_SOGR)
                if len(files) > 0:
                    k = 1
                else:
                    k = 0
            elif attrName == ProjectFile.TYPE_ORGANIZATION_MINUST:
                files = project.projectfile_set.all().filter(type=ProjectFile.TYPE_ORGANIZATION_MINUST)
                if len(files) > 0:
                    k = 1
                else:
                    k = 0
            elif attrName == ProjectFile.TYPE_ORGANIZATION_USTAV:
                files = project.projectfile_set.all().filter(type=ProjectFile.TYPE_ORGANIZATION_USTAV)
                if len(files) > 0:
                    k = 1
                else:
                    k = 0
            else:
                attr = getattr(obj, attrName)
                if attr:
                    if hasattr(attr, 'all') and isinstance(attr.all(), QuerySet):
                        if len(attr.all()) > 0:
                            k = 1
                        else:
                            k = 0
                    else:
                        k = 1
            count = count + k

        if len(fields) == 0:
            return 0

        return round((count * 100) / len(fields))

    """ Количество мероприятий в календарном плане """
    def events_count(self):
        count = self.events_count_num()
        s = self.get_num_ending(count, ['мероприятие', 'мероприятия', 'мероприятий'])
        return str(count) + " " + s

    def events_count_num(self):
        count = len(self.event_set.all())
        return count

    """ Количество статей в бюджете """
    def cost_count(self):
        count = self.cost_count_num()
        s = self.get_num_ending(count, ['статья', 'статьи', 'статей'])
        return str(count) + " " + s

    def cost_count_num(self):
        count = len(self.genericcost_set.all())
        return count

    @staticmethod
    def get_num_ending(number, endings):
        """
        param  number Integer Число на основе которого нужно сформировать окончание
        param  endings Array Массив слов или окончаний для чисел (1, 4, 5),
                например ['яблоко', 'яблока', 'яблок']
        """
        s_ending = ''
        number = number % 100
        if 11 <= number <= 19:
            s_ending = endings[2]
        else:
            i = number % 10
            if i == 1:
                s_ending = endings[0]
            elif i == 4:
                s_ending = endings[1]
            else:
                s_ending = endings[2]

        return s_ending
