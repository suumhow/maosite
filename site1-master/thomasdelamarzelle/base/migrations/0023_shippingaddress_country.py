# Generated by Django 3.0.3 on 2020-08-05 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20200804_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]