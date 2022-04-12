# Generated by Django 3.1 on 2022-04-10 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meteorvendor', '0005_auto_20220401_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]