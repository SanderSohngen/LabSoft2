# Generated by Django 5.0.3 on 2024-04-16 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_portal', '0003_remove_customuser_account_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='professional_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Professional Name'),
        ),
    ]
