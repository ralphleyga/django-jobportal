from django.contrib import admin

from .models import (Job,
                     JobQuestion,
                     Applicant,
                     ApplicantAnwer
                     )


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


class ApplicantAnswerInline(admin.TabularInline):
    model = ApplicantAnwer


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'job', 'created']
    
    inlines = [
        ApplicantAnswerInline
    ]


@admin.register(ApplicantAnwer)
class ApplicantAnwerAdmin(admin.ModelAdmin):
    list_display = ('id',)