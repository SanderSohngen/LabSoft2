# Generated by Django 4.2.11 on 2024-04-08 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer_portal', '0002_timeslot_delete_userdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('hashed_password', models.CharField(max_length=50)),
            ],
        ),
    ]