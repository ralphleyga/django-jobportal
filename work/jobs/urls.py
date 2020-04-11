from django.urls import path

from .views import (BrowseJobsView,
                    JobDetail,
                    JobFormView
                    )

app_name = 'jobs'

urlpatterns = [
    path('', BrowseJobsView.as_view(), name='browse'),
    path('detail/', JobDetail.as_view(), name='detail'),
    path('form/', JobFormView.as_view(), name='form'),

]
