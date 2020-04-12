from django.views.generic import (
    TemplateView,
    FormView,
    ListView,
    DetailView,
    CreateView,
    UpdateView
    )
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


class JobDetail(DetailView):
    template_name = 'jobs/job_detail.html'
    model = Job
    queryset = Job.objects.filter(archived=False, draft=False)


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    template_name = 'jobs/job_form.html'
    form_class = JobForm
    success_url = reverse_lazy('jobs:browse')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    template_name = 'jobs/job_form.html'
    form_class = JobForm
    success_url = reverse_lazy('jobs:browse')
    
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
    queryset = Job.objects.all()

    def get_queryset(self):
        """Job owner can archive/restore 
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if self.object.archived:
            self.object.archived = False
        else:
            self.object.archived = True

        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)