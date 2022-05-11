from django import forms
from apps.project.models import Project, Comment
from apps.expert.models import Expert
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple

class AssignExpertsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssignExpertsForm, self).__init__(*args, **kwargs)
        project = self.instance
        Expert.contest = project.contest
        self.fields['experts'].queryset = Expert.objects.filter(profile__directions__id=project.direction_id)

    class Meta:
        model = Project
        fields = ('experts',)
        

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = False
