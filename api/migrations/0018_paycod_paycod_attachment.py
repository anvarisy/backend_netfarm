# Generated by Django 3.0.10 on 2020-11-07 02:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20201103_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='paycod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_date', models.DateField(default=django.utils.timezone.now)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
        migrations.CreateModel(
            name='paycod_attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to='cod_attachment')),
                ('paycod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.paycod')),
            ],
        ),
    ]
