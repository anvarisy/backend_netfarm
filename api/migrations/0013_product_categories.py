# Generated by Django 3.0.10 on 2020-11-02 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_product_category_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(through='api.product_category', to='api.category'),
        ),
    ]
