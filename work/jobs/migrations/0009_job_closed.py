# Generated by Django 3.0.5 on 2020-04-13 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_job_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]