# Generated by Django 3.0.10 on 2020-11-02 07:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20201102_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
