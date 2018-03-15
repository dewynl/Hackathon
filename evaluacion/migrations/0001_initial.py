# Generated by Django 2.0.3 on 2018-03-15 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Criterio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explicacion', models.TextField(max_length=70)),
                ('tipo_jurado', models.SmallIntegerField(choices=[(1, 'JURADO TECNICO'), (2, 'JURADO NO TECNICO')])),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15)),
                ('participante1', models.CharField(max_length=25)),
                ('participante2', models.CharField(max_length=25)),
                ('participante3', models.CharField(max_length=25)),
                ('puntuacion', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Jurado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
                ('tipo', models.SmallIntegerField(choices=[(1, 'JURADO TECNICO'), (2, 'JURADO NO TECNICO')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]