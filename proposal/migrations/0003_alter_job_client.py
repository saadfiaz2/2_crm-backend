# Generated by Django 5.1 on 2024-09-10 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0002_job_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='client',
            field=models.CharField(max_length=255),
        ),
    ]
