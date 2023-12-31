# Generated by Django 4.2.3 on 2023-08-01 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('serialNumber', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('positionY', models.FloatField()),
                ('positionX', models.FloatField()),
                ('lastUpdate', models.DateTimeField()),
            ],
            options={
                'ordering': ['lastUpdate'],
            },
        ),
        migrations.CreateModel(
            name='Pilot',
            fields=[
                ('pilotId', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=64)),
                ('lastName', models.CharField(max_length=64)),
                ('phoneNumber', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=128)),
                ('lastAppearance', models.DateTimeField()),
                ('closestDistance', models.FloatField(blank=True)),
                ('drone', models.ForeignKey(db_column='serialNumber', on_delete=django.db.models.deletion.CASCADE, to='birdnest_app.drone')),
            ],
            options={
                'ordering': ['closestDistance'],
            },
        ),
    ]
