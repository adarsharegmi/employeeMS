# Generated by Django 3.0.8 on 2020-07-15 13:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='project',
            table='projects',
        ),
    ]
