# Generated by Django 2.1.15 on 2020-09-30 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id_category', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name_category', models.CharField(max_length=120)),
                ('show_homepage', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='tenant',
            fields=[
                ('id_tenant', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name_tenant', models.CharField(max_length=70)),
                ('address_tenant', models.TextField()),
                ('owner_tenant', models.CharField(max_length=100)),
            ],
        ),
    ]
