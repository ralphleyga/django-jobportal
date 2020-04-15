from django import forms

from .models import (
    Job,
    JobQuestion,
    POSITION_TYPE,
    WORK_ENVIRONMENT,
    Applicant,
    ApplicantAnwer)


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('user', 'archived', 'slug', 'closed')


class JobFilterForm(forms.ModelForm):
    
    class Meta:
        model = Job
        fields = ('country', 'work_environment', 'position')


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('name', 'email', 'cover_letter', 'document')


class ApplicantAnwerForm(forms.ModelForm):

    # question = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = ApplicantAnwer
        fields = ('question', 'answer')