from django.views.generic import (
    TemplateView,
    FormView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View
    )
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.forms import formset_factory

from .filters import JobFilter
from .forms import (
        JobForm,
        JobFilterForm,
        JobApplicationForm,
        ApplicantAnwerForm
    )
from .models import (
        Job,
        JobQuestion,
        Applicant,
        ApplicantAnwer
    )


class ActiveMenuMixin(object):
    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        context_data.update(self.active_menu)
        return context_data

class BrowseJobsView(ActiveMenuMixin, ListView):
    model = Job
    template_name = 'jobs/browse_jobs.html'
    queryset = Job.objects.filter(draft=False, archived=False).order_by('-created')
    form_class = JobFilterForm()
    paginate_by = 10
    header_title = 'Browse Jobs'
    active_menu = {}
    
    def get_queryset(self):
        queryset = super().get_queryset()
        qry = JobFilter(self.request.GET, queryset=queryset).qs
        return qry
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        context_data.update({
            'form': JobFilterForm(self.request.GET),
            'header_title': self.header_title
        })
        return context_data


class MyJobsView(BrowseJobsView):
    template_name = 'jobs/my_jobs.html'
    queryset = Job.objects.filter(archived=False).order_by('-created')
    header_title = 'Posted'
    active_menu = {'is_manage': True}
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        qry = JobFilter(self.request.GET, queryset=queryset).qs
        return qry


class MyJobsArchivedView(MyJobsView):
    queryset = Job.objects.filter(archived=True).order_by('-created')
    header_title = 'Archived'
    active_menu = {'is_archived': True}


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


class JobCreateView(LoginRequiredMixin, ActiveMenuMixin, SuccessMessageMixin, CreateView):
    model = Job
    template_name = 'jobs/job_form.html'
    form_class = JobForm
    success_url = reverse_lazy('jobs:manage')
    success_message = 'Job successfully created.'
    active_menu = {'is_create': True}
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Job
    template_name = 'jobs/job_form.html'
    form_class = JobForm
    success_url = reverse_lazy('jobs:manage')
    success_message = 'Job successfully updated.'
    
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
        next = request.GET.get('next')
        self.object = self.get_object()
        status = 'archived'
        
        if self.object.user != request.user:
            raise Http404
        
        if self.object.archived:
            self.object.archived = False
            status = 'restored'
        else:
            self.object.archived = True

        self.object.save()
        messages.add_message(request, messages.INFO, f'Job successfully {status}.')
        
        if not next:
            next = reverse_lazy('jobs:manage')

        return HttpResponseRedirect(next)
    

class JobCloseView(LoginRequiredMixin, JobDetail):
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        status = 'set to closed'
        
        if self.object.user != request.user:
            raise Http404
        
        if self.object.closed:
            self.object.closed = False
            status = 'open'
        else:
            self.object.closed = True

        self.object.save()
        messages.add_message(request, messages.INFO, f'Job successfully {status}.')
        return HttpResponseRedirect(reverse_lazy('jobs:manage'))


class JobDraftView(LoginRequiredMixin, JobDetail):
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        status = 'set to draft'
        
        if self.object.user != request.user:
            raise Http404
        
        if self.object.draft:
            self.object.draft = False
            status = 'published'
        else:
            self.object.draft = True

        self.object.save()
        messages.add_message(request, messages.INFO, f'Job successfully {status}.')
        return HttpResponseRedirect(reverse_lazy('jobs:manage'))


class QuestionFormMixin(object):
    model = JobQuestion
    template_name = 'jobs/ajax_question_form.html'
    fields = ('question',)

    def get_success_url(self):
        job = Job.objects.get(slug=self.kwargs.get('slug'))
        return reverse_lazy('jobs:detail', args=[job.slug])


class QuestionUpdateView(LoginRequiredMixin, SuccessMessageMixin, QuestionFormMixin, UpdateView):
    
    success_message = 'Question successfully updated.'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(job__user=self.request.user)
        return queryset


class QuestionCreateView(LoginRequiredMixin, SuccessMessageMixin, QuestionFormMixin, CreateView):
    success_message = 'Question successfully created.'

    def form_valid(self, form):
        job = Job.objects.get(slug=self.kwargs.get('slug'))
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.job = job
        self.object.save()
        return super().form_valid(form)


class QuestionDeleteView(LoginRequiredMixin, View):
    success_message = 'Warning: Question has been deleted.'
    
    def get(self, request, **kwargs):
        question = JobQuestion.objects.get(id=kwargs['pk'])
        
        if question.job.user != request.user:
            raise
        
        question.delete()
        messages.add_message(request, messages.INFO, self.success_message)
        return HttpResponseRedirect(reverse_lazy('jobs:detail', args=[question.job.slug]))


class SubmitApplicationView(TemplateView):
    
    template_name = 'jobs/ajax_send_application.html'
    form_class = JobApplicationForm
    success_message = 'You have successfully sent your application.'

    def get(self, request, **kwargs):
        form = self.form_class()
        job = get_object_or_404(Job, slug=kwargs.get('slug'))
        jobs_count = job.jobquestion_set.all().count()
        ApplicantAnwerFormSet = formset_factory(ApplicantAnwerForm, extra=jobs_count, max_num=jobs_count)
        initial_data = []
        for jq in job.jobquestion_set.all():
            initial_data.append({
                'question': jq.id,
            })
        
        return self.render_to_response({
            'form': form,
            'form_set': ApplicantAnwerFormSet(initial=initial_data),
            'job': job
        })
        
        
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        job = get_object_or_404(Job, slug=kwargs.get('slug'))
        jobs_count = job.jobquestion_set.all().count()
        ApplicantAnwerFormSet = formset_factory(ApplicantAnwerForm)
        formset = ApplicantAnwerFormSet(data=request.POST)
        
        if form.is_valid():
            applicant = form.save(commit=False)

            if request.user.is_authenticated:
                applicant.user = request.user
            applicant.job = job
            applicant.save()

        if formset.is_valid():
            for answer_form in formset:
                if answer_form.is_valid():
                    answer = answer_form.save(commit=False)
                    answer.applicant = applicant
                    answer.save()
            messages.add_message(request, messages.INFO, self.success_message)
        return HttpResponseRedirect(reverse_lazy('jobs:detail', args=[job.slug]))


class ApplicantView(LoginRequiredMixin, TemplateView):
    
    template_name = 'jobs/ajax_view_applicant.html'
    
    def get(self, request, **kwargs):
        applicant = get_object_or_404(Applicant, id=kwargs['id'])
        
        if applicant.job.user != request.user:
            raise Http404

        return self.render_to_response({
            'applicant': applicant
        })
    
    def post(self, request, **kwargs):
        applicant = get_object_or_404(Applicant, id=kwargs['id'])

        if applicant.job.user != request.user:
            raise Http404

        if 'interview' in request.POST:
            applicant.applicant_status = 'interview'
        elif 'reject' in request.POST:
            applicant.applicant_status = 'rejected'

        applicant.save()
        messages.add_message(request, messages.INFO, f'You have success set the applicant to {applicant.applicant_status}')
        return HttpResponseRedirect(reverse_lazy('jobs:detail', args=[kwargs['slug']]))