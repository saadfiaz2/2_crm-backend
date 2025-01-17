# Generated by Django 5.1 on 2024-10-17 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_leave'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='is_approved_by_hr',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='leave',
            name='is_approved_by_lead',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='annual_leave_quota',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='casual_leave_quota',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='sick_leave_quota',
            field=models.FloatField(default=0),
        ),
    ]
