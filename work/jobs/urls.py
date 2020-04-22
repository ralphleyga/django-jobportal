from django.urls import path

from .views import (BrowseJobsView,
                    JobDetail,
                    JobCreateView,
                    JobUpdateView,
                    JobArchiveView,
                    MyJobsView,
                    MyJobsArchivedView,
                    JobDraftView,
                    JobCloseView,
                    JobAskPaymentView,
                    
                    JobActivateTrialView,
                    JobActivateOptionView,
                    
                    QuestionUpdateView,
                    QuestionCreateView,
                    QuestionDeleteView,
                    
                    SubmitApplicationView,
                    ApplicantView,
                    ApplicationListView
                    )

app_name = 'jobs'

urlpatterns = [
    path('applicants/', ApplicationListView.as_view(), name='applicants'),
    path('create/', JobCreateView.as_view(), name='create'),
    path('manage/', MyJobsView.as_view(), name='manage'),
    path('archived/', MyJobsArchivedView.as_view(), name='archived'),
    path('update/<slug:slug>/', JobUpdateView.as_view(), name='update'),
    path('archive/<slug:slug>/', JobArchiveView.as_view(), name='archive'),
    path('status/<slug:slug>/', JobCloseView.as_view(), name='status'),
    path('draft/<slug:slug>/', JobDraftView.as_view(), name='draft'),
    
    # questions
    path('<slug:slug>/question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    path('<slug:slug>/question/<int:pk>/update/', QuestionUpdateView.as_view(), name='question_update'),
    path('<slug:slug>/question/', QuestionCreateView.as_view(), name='question_create'),


    path('<slug:slug>/apply/', SubmitApplicationView.as_view(), name='submit_application'),
    path('<slug:slug>/payment/', JobAskPaymentView.as_view(), name='ask_payment'),
    path('<slug:slug>/publish-option/', JobActivateOptionView.as_view(), name='activate_option'),
    path('<slug:slug>/applicant/<int:id>/', ApplicantView.as_view(), name='view_application'),
    path('<slug:slug>/activate/trial/', JobActivateTrialView.as_view(), name='activate_trial'),
    path('<slug:slug>/', JobDetail.as_view(), name='detail'),

    path('', BrowseJobsView.as_view(), name='browse'),

]
