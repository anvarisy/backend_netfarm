# Generated by Django 3.0.10 on 2021-02-03 01:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_tenant_tenant_city_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_status',
            name='transaction_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
