# Generated by Django 5.1 on 2024-10-29 09:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_medium_source_lead_medium_lead_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
