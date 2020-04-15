from django import template
register = template.Library()

from jobs.models import JobQuestion

@register.filter
def job_question(value):
    return JobQuestion.objects.get(id=value).question