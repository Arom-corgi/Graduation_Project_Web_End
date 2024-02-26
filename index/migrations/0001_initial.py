# Generated by Django 5.0.2 on 2024-02-23 01:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('is_bind', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '设备',
                'verbose_name_plural': '设备',
                'db_table': '设备',
                'ordering': ['unique_id'],
            },
        ),
        migrations.CreateModel(
            name='DeviceData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('heart_rate', models.IntegerField(blank=True, null=True)),
                ('blood_oxygen', models.IntegerField(blank=True, null=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='index.device')),
            ],
            options={
                'verbose_name': '设备数据',
                'verbose_name_plural': '设备数据',
                'db_table': '设备数据',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='BindDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bind_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bind_devices', to=settings.AUTH_USER_MODEL)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bind_users', to='index.device')),
            ],
            options={
                'verbose_name': '绑定设备',
                'verbose_name_plural': '绑定设备',
                'db_table': '绑定设备',
                'unique_together': {('user', 'device')},
            },
        ),
    ]
