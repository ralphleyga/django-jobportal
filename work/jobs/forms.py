from django import forms

from .models import Job, JobQuestion

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('user', 'archived', 'draft', 'slug')