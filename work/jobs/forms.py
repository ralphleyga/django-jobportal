from django import forms

from .models import Job, JobQuestion, POSITION_TYPE, WORK_ENVIRONMENT

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('user', 'archived', 'slug', 'closed')
        

class JobFilterForm(forms.ModelForm):
    
    class Meta:
        model = Job
        fields = ('country', 'work_environment', 'position')
