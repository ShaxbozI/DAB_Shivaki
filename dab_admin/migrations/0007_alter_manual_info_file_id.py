# Generated by Django 5.1.3 on 2025-01-13 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dab_admin', '0006_manual_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manual_info',
            name='file_id',
            field=models.TextField(),
        ),
    ]
