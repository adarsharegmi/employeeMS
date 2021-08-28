# Generated by Django 3.0.8 on 2021-08-28 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='networkactivity',
            options={'default_related_name': 'domains_activity_set'},
        ),
        migrations.AlterModelOptions(
            name='screenshotactivity',
            options={'default_related_name': 'screenshot_set', 'verbose_name': 'screenshot', 'verbose_name_plural': 'screenshots'},
        ),
        migrations.AlterField(
            model_name='networkactivity',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains_activity_set', to=settings.AUTH_USER_MODEL, verbose_name='employee the activity was made by'),
        ),
        migrations.AlterField(
            model_name='screenshotactivity',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshot_set', to=settings.AUTH_USER_MODEL, verbose_name='employee the activity was made by'),
        ),
    ]
