# Generated by Django 3.1 on 2022-04-10 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meteorvendor', '0006_owner_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='ownerpassword',
            field=models.CharField(max_length=30, null=True),
        ),
    ]