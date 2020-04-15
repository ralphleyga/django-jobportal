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
                    
                    QuestionUpdateView,
                    QuestionCreateView,
                    QuestionDeleteView,
                    
                    SubmitApplicationView,
                    )

app_name = 'jobs'

urlpatterns = [
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
    path('<slug:slug>/', JobDetail.as_view(), name='detail'),

    path('', BrowseJobsView.as_view(), name='browse'),

]
