# Generated by Django 3.0.3 on 2020-07-29 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_student_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_pic',
            field=models.ImageField(blank=True, default='logo.jpg', null=True, upload_to=''),
        ),
    ]
