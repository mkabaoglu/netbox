# Generated by Django 3.1.4 on 2021-01-05 11:38

import django.contrib.postgres.fields
import django.core.serializers.json
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0053_rename_webhook_obj_type'),
        ('virtualization', '0019_standardize_name_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('name', models.CharField(max_length=100)),
                ('protocol', models.CharField(max_length=50)),
                ('ports', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(65535)]), size=None)),
                ('status', models.CharField(default='active', max_length=50)),
                ('Domain', models.CharField(blank=True, max_length=70)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicess', to='virtualization.cluster')),
                ('tags', taggit.managers.TaggableManager(related_name='Services', through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('protocol', 'ports', 'pk'),
            },
        ),
    ]