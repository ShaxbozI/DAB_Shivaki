# Generated by Django 5.1.3 on 2025-01-12 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dab_admin', '0004_type_errors_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot_users',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]
