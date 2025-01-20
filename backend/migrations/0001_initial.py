# Generated by Django 5.1.4 on 2025-01-20 15:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Observer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observers', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.object')),
                ('_description', models.CharField(max_length=4294967295, null=True)),
                ('cols', models.IntegerField(null=True)),
                ('rows', models.IntegerField(null=True)),
                ('cell_size', models.IntegerField(null=True)),
                ('bg_color', models.CharField(max_length=7, null=True)),
                ('_game_mode_active', models.BooleanField(null=True)),
                ('_start_time', models.FloatField(null=True)),
                ('_tick_interval', models.FloatField(null=True)),
                ('_notification_interval', models.FloatField(null=True)),
                ('_tick_count', models.IntegerField(null=True)),
            ],
            bases=('backend.object',),
        ),
        migrations.CreateModel(
            name='Fuel',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.object')),
                ('row', models.IntegerField(blank=True, null=True)),
                ('col', models.IntegerField(blank=True, null=True)),
                ('_MAP', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.map')),
            ],
            options={
                'abstract': False,
            },
            bases=('backend.object',),
        ),
        migrations.CreateModel(
            name='Diagonal',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.object')),
                ('row', models.IntegerField(blank=True, null=True)),
                ('col', models.IntegerField(blank=True, null=True)),
                ('rotation', models.IntegerField(null=True)),
                ('_MAP', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.map')),
            ],
            options={
                'abstract': False,
            },
            bases=('backend.object',),
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.object')),
                ('_DRIVER', models.CharField(max_length=4294967295, null=True)),
                ('_MODEL', models.CharField(max_length=4294967295, null=True)),
                ('_ACCELERATION_RATE', models.FloatField(null=True)),
                ('_FUEL_CONSUMPTION_RATE', models.FloatField(null=True)),
                ('_DECELERATION_RATE', models.FloatField(null=True)),
                ('_STEER_RATE', models.FloatField(null=True)),
                ('_MAX_SPEED', models.FloatField(null=True)),
                ('_MAX_FUEL', models.FloatField(null=True)),
                ('_user', models.CharField(max_length=4294967295, null=True)),
                ('_position', models.JSONField(null=True)),
                ('_angle', models.FloatField(null=True)),
                ('_speed', models.FloatField(null=True)),
                ('_fuel', models.FloatField(null=True)),
                ('_accelerate', models.BooleanField(null=True)),
                ('_brake', models.BooleanField(null=True)),
                ('_turn_clockwise', models.BooleanField(null=True)),
                ('_turn_counterclockwise', models.BooleanField(null=True)),
                ('_running', models.BooleanField(null=True)),
                ('_MAP', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.map')),
            ],
            options={
                'abstract': False,
            },
            bases=('backend.object',),
        ),
        migrations.CreateModel(
            name='Booster',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.object')),
                ('row', models.IntegerField(blank=True, null=True)),
                ('col', models.IntegerField(blank=True, null=True)),
                ('_MAP', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.map')),
            ],
            options={
                'abstract': False,
            },
            bases=('backend.object',),
        ),
        migrations.CreateModel(
            name='Rock',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.object')),
                ('row', models.IntegerField(blank=True, null=True)),
                ('col', models.IntegerField(blank=True, null=True)),
                ('_MAP', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.map')),
            ],
            options={
                'abstract': False,
            },
            bases=('backend.object',),
        ),
        migrations.CreateModel(
            name='Straight',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.object')),
                ('row', models.IntegerField(blank=True, null=True)),
                ('col', models.IntegerField(blank=True, null=True)),
                ('rotation', models.IntegerField(null=True)),
                ('_MAP', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.map')),
            ],
            options={
                'abstract': False,
            },
            bases=('backend.object',),
        ),
        migrations.CreateModel(
            name='Turn90',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.object')),
                ('row', models.IntegerField(blank=True, null=True)),
                ('col', models.IntegerField(blank=True, null=True)),
                ('rotation', models.IntegerField(null=True)),
                ('_MAP', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.map')),
            ],
            options={
                'abstract': False,
            },
            bases=('backend.object',),
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.object')),
                ('y', models.FloatField(null=True)),
                ('x', models.FloatField(null=True)),
                ('height', models.FloatField(null=True)),
                ('width', models.FloatField(null=True)),
                ('user', models.CharField(max_length=4294967295, null=True)),
                ('_description', models.CharField(max_length=4294967295, null=True)),
                ('original_map', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.map')),
            ],
            bases=('backend.object',),
        ),
    ]
