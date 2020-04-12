from django.views.generic import (
    TemplateView,
    FormView,
    ListView,
    DetailView,
    CreateView,
    UpdateView
    )
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import JobFilter
from .forms import JobForm, JobFilterForm
from .models import Job


class BrowseJobsView(ListView):
    model = Job
    template_name = 'jobs/browse_jobs.html'
    queryset = Job.objects.filter(draft=False, archived=False).order_by('-created')
    form_class = JobFilterForm()
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        qry = JobFilter(self.request.GET, queryset=queryset).qs
        return qry
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        context_data.update({
            'form': JobFilterForm(self.request.GET)
        })
        return context_data


class MyJobsView(BrowseJobsView):
    template_name = 'jobs/my_jobs.html'
    queryset = Job.objects.filter(archived=False).order_by('-created')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        qry = JobFilter(self.request.GET, queryset=queryset).qs
        return qry


class JobDetail(DetailView):
    template_name = 'jobs/job_detail.html'
    model = Job

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        if obj.user == self.request.user:
            return obj
        
        if obj.draft:
            raise Http404
        
        if obj.archived:
            raise Http404

        return obj


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    template_name = 'jobs/job_form.html'
    form_class = JobForm
    success_url = reverse_lazy('jobs:manage')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    template_name = 'jobs/job_form.html'
    form_class = JobForm
    success_url = reverse_lazy('jobs:manage')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

class JobArchiveView(LoginRequiredMixin, JobDetail):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if self.object.user != request.user:
            raise Http404
        
        if self.object.archived:
            self.object.archived = False
        else:
            self.object.archived = True

        self.object.save()
        return HttpResponseRedirect(reverse_lazy('jobs:manage'))