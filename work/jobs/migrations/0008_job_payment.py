# Generated by Django 3.0.5 on 2020-04-12 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_job_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='payment',
            field=models.CharField(choices=[('fixed_price', 'Fixed Price'), ('hourly', 'Hourly'), ('monthly', 'Monthly')], max_length=200, null=True),
        ),
    ]
