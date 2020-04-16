from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from jobs.models import Job

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get(self, request):
        context = {
            'jobs': Job.objects.filter(archived=False, draft=False).order_by('-created')[:3]
        }
        return self.render_to_response(context)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get(self, request):
        context = {
            'jobs': Job.objects.filter(user=request.user, archived=False).order_by('-created')[:3]
        }
        return self.render_to_response(context)