# Generated by Django 5.1 on 2024-08-28 06:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Employee', 'Employee'), ('HR', 'HR'), ('Admin', 'Admin'), ('Leads', 'Leads'), ('Project Manager', 'Project Manager')], default='Employee', max_length=20)),
                ('cnic', models.CharField(max_length=13, unique=True)),
                ('date_of_joining', models.DateField()),
                ('designation', models.CharField(max_length=100)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('mobile_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('emergency_phone_number', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('skills', models.ManyToManyField(blank=True, related_name='profiles', to='users.skill')),
            ],
        ),
    ]
