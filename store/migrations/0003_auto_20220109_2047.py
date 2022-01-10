# Generated by Django 3.2.3 on 2022-01-10 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title']},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='unit_price',
        ),
    ]
