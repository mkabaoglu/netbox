# Generated by Django 3.1.4 on 2021-01-04 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0003_auto_20210103_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='r_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='record',
            name='r_value',
            field=models.CharField(max_length=50),
        ),
    ]