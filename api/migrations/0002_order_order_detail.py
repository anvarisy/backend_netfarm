# Generated by Django 3.0.10 on 2020-10-12 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('order_id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('total', models.BigIntegerField()),
                ('date_update', models.DateField()),
                ('status', models.CharField(max_length=30)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user_client')),
            ],
        ),
        migrations.CreateModel(
            name='order_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_product', models.IntegerField()),
                ('total', models.BigIntegerField()),
                ('date_update', models.DateField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
    ]
