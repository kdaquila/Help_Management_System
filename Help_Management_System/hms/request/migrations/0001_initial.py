# Generated by Django 2.2.5 on 2019-11-10 01:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(default='', max_length=100)),
                ('password', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now)),
                ('role', models.CharField(default='user', max_length=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=100)),
                ('title', models.CharField(default='', max_length=100)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Group')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.User')),
                ('tags', models.ManyToManyField(to='request.Tag')),
            ],
        ),
    ]
