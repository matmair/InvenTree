# Generated by Django 3.2.19 on 2023-06-29 14:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0019_returnorderreport_metadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockLocationReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('name', models.CharField(help_text='Template name', max_length=100, verbose_name='Name')),
                ('template', models.FileField(help_text='Report template file', upload_to='report', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['html', 'htm'])], verbose_name='Template')),
                ('description', models.CharField(help_text='Report template description', max_length=250, verbose_name='Description')),
                ('revision', models.PositiveIntegerField(default=1, editable=False, help_text='Report revision number (auto-increments)', verbose_name='Revision')),
                ('filename_pattern', models.CharField(default='report.pdf', help_text='Pattern for generating report filenames', max_length=100, verbose_name='Filename Pattern')),
                ('enabled', models.BooleanField(default=True, help_text='Report template is enabled', verbose_name='Enabled')),
                ('filters', models.CharField(blank=True, help_text='stock location query filters (comma-separated list of key=value pairs)', max_length=250, verbose_name='Filters')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
