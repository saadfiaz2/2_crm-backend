# Generated by Django 5.1 on 2024-10-14 12:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_profile_account_holder_name_profile_account_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(choices=[('Casual', 'Casual'), ('Sick', 'Sick'), ('Annual', 'Annual'), ('Umrah', 'Umrah'), ('Compensatory', 'Compensatory'), ('Parental', 'Parental'), ('Maternity', 'Maternity'), ('Bereavement', 'Bereavement')], max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('reason', models.TextField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to='users.profile')),
            ],
        ),
    ]