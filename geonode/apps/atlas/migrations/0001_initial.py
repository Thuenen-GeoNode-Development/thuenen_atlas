# Generated by Django 3.2.16 on 2023-03-21 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0034_auto_20200512_1431'),
        ('base', '0085_alter_resourcebase_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atlas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(max_length=128, unique=True)),
                ('primer', models.TextField(default='primer')),
                ('jumbotronBackgroundImage', models.ImageField(blank=True, null=True, upload_to='atlas/backgroundImage/%Y/%m', verbose_name='Atlas jumbotron background image')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='atlas/thumbs/%Y/%m', verbose_name='Atlas thumbnail')),
                ('jumbotronBackgroundMovie', models.FileField(blank=True, null=True, upload_to='atlas/mov/%Y/%m', verbose_name='Atlas jumbotron background movie')),
                ('content', models.TextField(default='content')),
                ('group', models.ManyToManyField(blank=True, null=True, related_name='group_collections', to='groups.GroupProfile')),
                ('resource', models.ManyToManyField(blank=True, null=True, related_name='resource_collections', to='base.ResourceBase')),
            ],
        ),
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
        migrations.CreateModel(
            name='AtlasCustomAppListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(default=0)),
                ('atlas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atlas.atlas')),
                ('customApp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atlas.customapplication')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
