from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    UpdateView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin

from jobs.models import Job, Applicant

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get(self, request):
        context = {
            'jobs': Job.objects.filter(archived=False, draft=False).order_by('-created')[:3],
        }
        return self.render_to_response(context)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get(self, request):
        context = {
            'jobs': Job.objects.filter(user=request.user, archived=False).order_by('-created')[:10],
            'applicants': Applicant.objects.filter(job__user=request.user, job__archived=False, job__draft=False).order_by('-created')[:10]
        }
        return self.render_to_response(context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/ajax_profile_update.html'