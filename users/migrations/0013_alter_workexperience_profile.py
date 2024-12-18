# Generated by Django 5.1 on 2024-10-18 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_workexperience_end_date_workexperience_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperience',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='users.profile'),
        ),
    ]
