# Generated by Django 3.0.3 on 2020-08-04 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_product_digital'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='zipcode',
            new_name='ziploc',
        ),
    ]
