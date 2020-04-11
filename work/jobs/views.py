from django.views.generic import TemplateView, FormView

from .forms import JobForm


class BrowseJobsView(TemplateView):
    
    template_name = 'jobs/browse_jobs.html'
    

class JobDetail(TemplateView):
    template_name = 'jobs/job_detail.html'
    

class JobFormView(FormView):
    template_name = 'jobs/job_form.html'
    form_class = JobForm
    success_url = '/thanks/'