# Generated by Django 3.0.5 on 2020-04-11 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20200409_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='slug',
            field=models.SlugField(max_length=300, null=True),
        ),
    ]