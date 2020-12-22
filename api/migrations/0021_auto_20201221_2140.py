# Generated by Django 3.0.10 on 2020-12-21 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_detail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='api.product'),
        ),
    ]