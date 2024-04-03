# Generated by Django 4.2.7 on 2024-04-03 13:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('info_consulta', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('idade', models.IntegerField()),
                ('sexo', models.CharField(max_length=20)),
                ('peso', models.FloatField()),
                ('altura', models.FloatField()),
                ('restricoes_alimentares', models.TextField()),
                ('observacoes', models.TextField()),
                ('consultas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor_portal.consulta')),
            ],
        ),
    ]
