from django.urls import path

from .views import (BrowseJobsView,
                    JobDetail,
                    JobFormView,
                    JobCreateView,
                    JobUpdateView,
                    )

app_name = 'jobs'

urlpatterns = [
    path('form/', JobFormView.as_view(), name='form'),
    path('create/', JobCreateView.as_view(), name='create'),
    path('update/<slug:slug>/', JobUpdateView.as_view(), name='update'),

    path('<slug:slug>/', JobDetail.as_view(), name='detail'),

    path('', BrowseJobsView.as_view(), name='browse'),

]
