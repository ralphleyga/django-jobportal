from django.urls import path

from .views import (BrowseJobsView,
                    JobDetail,
                    JobCreateView,
                    JobUpdateView,
                    JobArchiveView
                    )

app_name = 'jobs'

urlpatterns = [
    path('create/', JobCreateView.as_view(), name='create'),
    path('update/<slug:slug>/', JobUpdateView.as_view(), name='update'),
    path('archive/<slug:slug>/', JobArchiveView.as_view(), name='archive'),

    path('<slug:slug>/', JobDetail.as_view(), name='detail'),

    path('', BrowseJobsView.as_view(), name='browse'),

]
