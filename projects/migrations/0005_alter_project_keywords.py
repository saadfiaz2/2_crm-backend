# Generated by Django 5.1 on 2024-09-02 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_project_logo_icon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='keywords',
            field=models.ManyToManyField(blank=True, null=True, related_name='projects', to='projects.keyword'),
        ),
    ]
