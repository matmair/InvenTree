# Generated by Django 3.2.19 on 2023-06-10 21:26

import django.core.validators
from django.db import migrations, models
import report.models


class Migration(migrations.Migration):

    replaces = [('report', '0001_initial'), ('report', '0002_delete_reporttemplate'), ('report', '0003_testreport_enabled'), ('report', '0004_auto_20200823_1104'), ('report', '0005_auto_20210119_0815'), ('report', '0006_reportsnippet'), ('report', '0007_auto_20210204_1617'), ('report', '0008_auto_20210204_2100'), ('report', '0009_testreport_revision'), ('report', '0010_auto_20210205_1201'), ('report', '0011_auto_20210212_2024'), ('report', '0012_buildreport'), ('report', '0013_testreport_include_installed'), ('report', '0014_purchaseorderreport_salesorderreport'), ('report', '0015_auto_20210403_1837'), ('report', '0016_auto_20210513_1303'), ('report', '0017_auto_20230317_0816'), ('report', '0018_returnorderreport'), ('report', '0019_returnorderreport_metadata')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.FileField(help_text='Report asset file', upload_to=report.models.rename_template, verbose_name='Asset')),
                ('description', models.CharField(help_text='Asset file description', max_length=250, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='ReportSnippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snippet', models.FileField(help_text='Report snippet file', upload_to= report.models.rename_template, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['html', 'htm'])], verbose_name='Snippet')),
                ('description', models.CharField(help_text='Snippet file description', max_length=250, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='BillOfMaterialsReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Template name', max_length=100, verbose_name='Name')),
                ('template', models.FileField(help_text='Report template file', upload_to=report.models.rename_template, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['html', 'htm'])], verbose_name='Template')),
                ('description', models.CharField(help_text='Report template description', max_length=250, verbose_name='Description')),
                ('revision', models.PositiveIntegerField(default=1, editable=False, help_text='Report revision number (auto-increments)', verbose_name='Revision')),
                ('enabled', models.BooleanField(default=True, help_text='Report template is enabled', verbose_name='Enabled')),
                ('filters', models.CharField(blank=True, help_text='Part query filters (comma-separated list of key=value pairs', max_length=250, verbose_name='Part Filters')),
                ('filename_pattern', models.CharField(default='report.pdf', help_text='Pattern for generating report filenames', max_length=100, verbose_name='Filename Pattern')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BuildReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Template name', max_length=100, verbose_name='Name')),
                ('template', models.FileField(help_text='Report template file', upload_to=report.models.rename_template, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['html', 'htm'])], verbose_name='Template')),
                ('description', models.CharField(help_text='Report template description', max_length=250, verbose_name='Description')),
                ('revision', models.PositiveIntegerField(default=1, editable=False, help_text='Report revision number (auto-increments)', verbose_name='Revision')),
                ('enabled', models.BooleanField(default=True, help_text='Report template is enabled', verbose_name='Enabled')),
                ('filters', models.CharField(blank=True, help_text='Build query filters (comma-separated list of key=value pairs', max_length=250, verbose_name='Build Filters')),
                ('filename_pattern', models.CharField(default='report.pdf', help_text='Pattern for generating report filenames', max_length=100, verbose_name='Filename Pattern')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Template name', max_length=100, verbose_name='Name')),
                ('template', models.FileField(help_text='Report template file', upload_to=report.models.rename_template, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['html', 'htm'])], verbose_name='Template')),
                ('description', models.CharField(help_text='Report template description', max_length=250, verbose_name='Description')),
                ('revision', models.PositiveIntegerField(default=1, editable=False, help_text='Report revision number (auto-increments)', verbose_name='Revision')),
                ('enabled', models.BooleanField(default=True, help_text='Report template is enabled', verbose_name='Enabled')),
                ('filters', models.CharField(blank=True, help_text='Purchase order query filters', max_length=250, verbose_name='Filters')),
                ('filename_pattern', models.CharField(default='report.pdf', help_text='Pattern for generating report filenames', max_length=100, verbose_name='Filename Pattern')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalesOrderReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Template name', max_length=100, verbose_name='Name')),
                ('template', models.FileField(help_text='Report template file', upload_to=report.models.rename_template, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['html', 'htm'])], verbose_name='Template')),
                ('description', models.CharField(help_text='Report template description', max_length=250, verbose_name='Description')),
                ('revision', models.PositiveIntegerField(default=1, editable=False, help_text='Report revision number (auto-increments)', verbose_name='Revision')),
                ('enabled', models.BooleanField(default=True, help_text='Report template is enabled', verbose_name='Enabled')),
                ('filters', models.CharField(blank=True, help_text='Sales order query filters', max_length=250, verbose_name='Filters')),
                ('filename_pattern', models.CharField(default='report.pdf', help_text='Pattern for generating report filenames', max_length=100, verbose_name='Filename Pattern')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Template name', max_length=100, verbose_name='Name')),
                ('template', models.FileField(help_text='Report template file', upload_to=report.models.rename_template, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['html', 'htm'])], verbose_name='Template')),
                ('description', models.CharField(help_text='Report template description', max_length=250, verbose_name='Description')),
                ('filters', models.CharField(blank=True, help_text='StockItem query filters (comma-separated list of key=value pairs)', max_length=250, verbose_name='Filters')),
                ('enabled', models.BooleanField(default=True, help_text='Report template is enabled', verbose_name='Enabled')),
                ('revision', models.PositiveIntegerField(default=1, editable=False, help_text='Report revision number (auto-increments)', verbose_name='Revision')),
                ('include_installed', models.BooleanField(default=False, help_text='Include test results for stock items installed inside assembled item', verbose_name='Include Installed Tests')),
                ('filename_pattern', models.CharField(default='report.pdf', help_text='Pattern for generating report filenames', max_length=100, verbose_name='Filename Pattern')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnOrderReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Template name', max_length=100, verbose_name='Name')),
                ('template', models.FileField(help_text='Report template file', upload_to=report.models.rename_template, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['html', 'htm'])], verbose_name='Template')),
                ('description', models.CharField(help_text='Report template description', max_length=250, verbose_name='Description')),
                ('revision', models.PositiveIntegerField(default=1, editable=False, help_text='Report revision number (auto-increments)', verbose_name='Revision')),
                ('filename_pattern', models.CharField(default='report.pdf', help_text='Pattern for generating report filenames', max_length=100, verbose_name='Filename Pattern')),
                ('enabled', models.BooleanField(default=True, help_text='Report template is enabled', verbose_name='Enabled')),
                ('filters', models.CharField(blank=True, help_text='Return order query filters', max_length=250, verbose_name='Filters')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
