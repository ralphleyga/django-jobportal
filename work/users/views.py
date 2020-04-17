from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    UpdateView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from jobs.models import Job, Applicant

from .models import User


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


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/ajax_profile_form.html'
    model = User
    fields = (
                'first_name',
                'last_name',
                'email',
                'logo',
                'company',
                'about',
                'website'
                )
    success_message = 'Profile Updated.'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

