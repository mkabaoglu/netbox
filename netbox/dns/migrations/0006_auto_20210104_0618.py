# Generated by Django 3.1.4 on 2021-01-04 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0005_auto_20210104_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='r_value',
            field=models.CharField(max_length=1000),
        ),
    ]
