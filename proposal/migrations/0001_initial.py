# Generated by Django 5.1 on 2024-09-04 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('budget', models.IntegerField(blank=True, null=True)),
                ('source_link', models.URLField()),
                ('description', models.TextField()),
                ('deadline', models.DateField(blank=True, null=True)),
            ],
        ),
    ]