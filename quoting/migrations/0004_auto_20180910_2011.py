# Generated by Django 2.1 on 2018-09-11 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoting', '0003_auto_20180910_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
