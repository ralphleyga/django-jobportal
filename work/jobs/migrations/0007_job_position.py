# Generated by Django 3.0.5 on 2020-04-12 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20200411_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='position',
            field=models.CharField(choices=[('constractor', 'Contractor'), ('employee', 'Employee'), ('monthly', 'Monthly'), ('intern', 'Intern'), ('freelancer', 'Freelancer')], max_length=50, null=True),
        ),
    ]
