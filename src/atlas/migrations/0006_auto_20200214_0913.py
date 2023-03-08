# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-14 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0005_auto_20200214_0117'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='A short title', max_length=128, unique=True)),
                ('info', models.TextField(default='some additional information displayed for this custom app')),
                ('url', models.URLField()),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='atlas/customAppThumbs/%Y/%m', verbose_name='thumbnail for the app')),
            ],
        ),
        migrations.AddField(
            model_name='atlas',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='atlas/thumbs/%Y/%m', verbose_name='Atlas thumbnail'),
        ),
        migrations.AlterField(
            model_name='atlas',
            name='documents',
            field=models.ManyToManyField(null=True, related_name='document_collections', to='documents.Document'),
        ),
        migrations.AlterField(
            model_name='atlas',
            name='jumbotronBackgroundImage',
            field=models.ImageField(blank=True, null=True, upload_to='atlas/backgroundImage/%Y/%m', verbose_name='Atlas jumbotron background image'),
        ),
        migrations.AlterField(
            model_name='atlas',
            name='jumbotronBackgroundMovie',
            field=models.FileField(blank=True, null=True, upload_to='atlas/mov/%Y/%m', verbose_name='Atlas jumbotron background movie'),
        ),
        migrations.AlterField(
            model_name='atlas',
            name='layers',
            field=models.ManyToManyField(null=True, related_name='layer_collections', to='layers.Layer'),
        ),
        migrations.AlterField(
            model_name='atlas',
            name='maps',
            field=models.ManyToManyField(null=True, related_name='map_collections', to='maps.Map'),
        ),
        migrations.AddField(
            model_name='atlas',
            name='customApps',
            field=models.ManyToManyField(null=True, related_name='customApp_collections', to='atlas.CustomApplication'),
        ),
    ]
