from django.contrib import admin

from .models import (Job,
                     JobQuestion,
                     Applicant)


class JobQuestionInline(admin.TabularInline):
    model = JobQuestion


class ApplicantInline(admin.TabularInline):
    model = Applicant

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'user')
    search_fields = ('title', 'description')
    readonly_fields = ('slug',)

    inlines = [
        JobQuestionInline,
        ApplicantInline
    ]
