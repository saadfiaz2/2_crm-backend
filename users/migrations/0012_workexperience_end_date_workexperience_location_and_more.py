# Generated by Django 5.1 on 2024-10-18 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_leave_is_approved_by_hr_leave_is_approved_by_lead_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workexperience',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workexperience',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='workexperience',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]