# Generated by Django 3.2.19 on 2023-06-19 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0002_auto_20230421_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='atlas',
            name='public',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
