# Generated by Django 5.1 on 2024-10-30 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_lead_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='division_lead',
        ),
    ]