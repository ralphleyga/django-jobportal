from django.db import models
from django_countries.fields import CountryField
from django.utils.text import slugify

WORK_ENVIRONMENT = (
    ('remote', 'Remote'),
    ('flexible', 'Flexible'),
    ('onsite', 'On Site')
)

APPLICANT_STATUS = (
    ('pending', 'Pending'),
    ('rejected', 'Rejected'),
    ('interview', 'Interview'),
    ('hire', 'Hire'),
)

PAYMENT_TYPE = (
    ('fixed_price', 'Fixed Price'),
    ('hourly', 'Hourly'),
    ('monthly', 'Monthly'),
)

POSITION_TYPE = (
    ('constractor', 'Contractor'),
    ('employee', 'Employee'),
    ('monthly', 'Monthly'),
    ('intern', 'Intern'),
    ('freelancer', 'Freelancer'),
)

class Job(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300, null=True, unique=True)
    description = models.TextField()
    
    location = models.CharField('City', max_length=200)
    country = CountryField(null=True)

    work_environment = models.CharField('Environment', choices=WORK_ENVIRONMENT, max_length=50)
    position = models.CharField(choices=POSITION_TYPE, max_length=50, null=True)
    payment = models.CharField(max_length=200, null=True, choices=PAYMENT_TYPE)
    salary_range = models.CharField('Salary', max_length=200, blank=True, null=True, help_text='Example:  $1000-2000 or $40 per hour')

    company = models.CharField(max_length=200, null=True)
    job_application_email = models.EmailField('Email', blank=True, null=True, help_text='Notify this email or blank to use default email') # Applications will be forwarded to this email
    job_link = models.URLField(blank=True, null=True, help_text='Enter external link or use our cover letter system') # blank if there's external link
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    def save(self, **kwargs):
        slug_str = f'{self.title}-at-{self.company}'
        self.slug = slugify(slug_str)
        super().save(**kwargs)
        
    def full_title(self):
        return f'{self.title} at {self.company}'

    def __str__(self):
        return self.title
    
    def get_pending_applicants(self):
        return self.applicant_set.filter(applicant_status='pending').order_by('created')
    
    def get_rejected_applicants(self):
        return self.applicant_set.filter(applicant_status='rejected').order_by('created')
    
    def get_interview_applicants(self):
        return self.applicant_set.filter(applicant_status='interview').order_by('created')


class JobQuestion(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    question = models.TextField()
    
    def __str__(self):
        return f'{self.question} - {self.job.title}'


def applicant_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'job_{instance.job.slug}/applicant_{instance.id}/{filename}'


class Applicant(models.Model):
    user = models.ForeignKey('users.User', blank=True, null=True, on_delete=models.DO_NOTHING)
    email = models.EmailField()
    name = models.CharField(max_length=200)

    cover_letter = models.TextField('Cover Letter')
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    applicant_status = models.CharField(max_length=50, choices=APPLICANT_STATUS)
    document = models.FileField(upload_to=applicant_directory_path, null=True, blank=True, help_text='Upload your resume or any supporting document')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.email} applied to {self.job.title}')
    
    class Meta:
        unique_together = ('job', 'email')


class ApplicantAnwer(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    answer = models.TextField()
    question = models.ForeignKey(JobQuestion, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.pk)