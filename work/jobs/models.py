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
    ('interview', 'Interview')
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


class JobQuestion(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    question = models.TextField()
    
    def __str__(self):
        return self.job.title


class Applicant(models.Model):
    user = models.ForeignKey('users.User', blank=True, null=True, on_delete=models.DO_NOTHING)
    email = models.EmailField()
    name = models.CharField(max_length=200)

    cover_letter = models.TextField()
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    applicant_status = models.CharField(max_length=50, choices=APPLICANT_STATUS)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} applied to {self.job.title}'
