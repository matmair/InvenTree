# Generated by Django 4.2.17 on 2025-01-05 12:47

import InvenTree.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import report.helpers
import report.models
import report.validators


class Migration(migrations.Migration):

    initial = True

    replaces = [('report', '0001_initial'), ('report', '0002_delete_reporttemplate'), ('report', '0003_testreport_enabled'), ('report', '0004_auto_20200823_1104'), ('report', '0005_auto_20210119_0815'), ('report', '0006_reportsnippet'), ('report', '0007_auto_20210204_1617'), ('report', '0008_auto_20210204_2100'), ('report', '0009_testreport_revision'), ('report', '0010_auto_20210205_1201'), ('report', '0011_auto_20210212_2024'), ('report', '0012_buildreport'), ('report', '0013_testreport_include_installed'), ('report', '0014_purchaseorderreport_salesorderreport'), ('report', '0015_auto_20210403_1837'), ('report', '0016_auto_20210513_1303'), ('report', '0017_auto_20230317_0816'), ('report', '0018_returnorderreport'), ('report', '0019_returnorderreport_metadata'), ('report', '0020_stocklocationreport'), ('report', '0021_auto_20231009_0144'), ('report', '0022_reporttemplate'), ('report', '0023_auto_20240421_0455'), ('report', '0024_delete_billofmaterialsreport_delete_buildreport_and_more'), ('report', '0025_labeltemplate'), ('report', '0026_auto_20240422_1301'), ('report', '0027_alter_labeltemplate_model_type_and_more'), ('report', '0028_labeltemplate_attach_to_model_and_more')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportAsset",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "asset",
                    models.FileField(
                        help_text="Report asset file",
                        upload_to=report.models.rename_template,
                        verbose_name="Asset",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        help_text="Asset file description",
                        max_length=250,
                        verbose_name="Description",
                    ),
                ),
            ],
            bases=(report.models.TemplateUploadMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ReportSnippet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "snippet",
                    models.FileField(
                        help_text="Report snippet file",
                        upload_to=report.models.rename_template,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["html", "htm"]
                            )
                        ],
                        verbose_name="Snippet",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        help_text="Snippet file description",
                        max_length=250,
                        verbose_name="Description",
                    ),
                ),
            ],
            bases=(report.models.TemplateUploadMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ReportTemplate",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        blank=True,
                        help_text="JSON metadata field, for use by external plugins",
                        null=True,
                        verbose_name="Plugin Metadata",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Template name", max_length=100, verbose_name="Name"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        help_text="Template description",
                        max_length=250,
                        verbose_name="Description",
                    ),
                ),
                (
                    "revision",
                    models.PositiveIntegerField(
                        default=1,
                        editable=False,
                        help_text="Revision number (auto-increments)",
                        verbose_name="Revision",
                    ),
                ),
                (
                    "attach_to_model",
                    models.BooleanField(
                        default=False,
                        help_text="Save report output as an attachment against linked model instance when printing",
                        verbose_name="Attach to Model on Print",
                    ),
                ),
                (
                    "filename_pattern",
                    models.CharField(
                        default="output.pdf",
                        help_text="Pattern for generating filenames",
                        max_length=100,
                        verbose_name="Filename Pattern",
                    ),
                ),
                (
                    "enabled",
                    models.BooleanField(
                        default=True,
                        help_text="Template is enabled",
                        verbose_name="Enabled",
                    ),
                ),
                (
                    "model_type",
                    models.CharField(
                        help_text="Target model type for template",
                        max_length=100,
                        validators=[report.validators.validate_report_model_type],
                    ),
                ),
                (
                    "filters",
                    models.CharField(
                        blank=True,
                        help_text="Template query filters (comma-separated list of key=value pairs)",
                        max_length=250,
                        validators=[report.validators.validate_filters],
                        verbose_name="Filters",
                    ),
                ),
                (
                    "template",
                    models.FileField(
                        help_text="Template file",
                        upload_to=report.models.rename_template,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["html", "htm"]
                            )
                        ],
                        verbose_name="Template",
                    ),
                ),
                (
                    "page_size",
                    models.CharField(
                        default=report.helpers.report_page_size_default,
                        help_text="Page size for PDF reports",
                        max_length=20,
                        verbose_name="Page Size",
                    ),
                ),
                (
                    "landscape",
                    models.BooleanField(
                        default=False,
                        help_text="Render report in landscape orientation",
                        verbose_name="Landscape",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("name", "model_type")},
            },
            bases=(
                report.models.TemplateUploadMixin,
                InvenTree.models.PluginValidationMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="ReportOutput",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "items",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Number of items to process",
                        verbose_name="Items",
                    ),
                ),
                (
                    "complete",
                    models.BooleanField(
                        default=False,
                        help_text="Report generation is complete",
                        verbose_name="Complete",
                    ),
                ),
                (
                    "progress",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Report generation progress",
                        verbose_name="Progress",
                    ),
                ),
                (
                    "output",
                    models.FileField(
                        blank=True,
                        help_text="Generated output file",
                        null=True,
                        upload_to="report/output",
                        verbose_name="Output File",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="report.reporttemplate",
                        verbose_name="Report Template",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="LabelTemplate",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        blank=True,
                        help_text="JSON metadata field, for use by external plugins",
                        null=True,
                        verbose_name="Plugin Metadata",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Template name", max_length=100, verbose_name="Name"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        help_text="Template description",
                        max_length=250,
                        verbose_name="Description",
                    ),
                ),
                (
                    "revision",
                    models.PositiveIntegerField(
                        default=1,
                        editable=False,
                        help_text="Revision number (auto-increments)",
                        verbose_name="Revision",
                    ),
                ),
                (
                    "attach_to_model",
                    models.BooleanField(
                        default=False,
                        help_text="Save report output as an attachment against linked model instance when printing",
                        verbose_name="Attach to Model on Print",
                    ),
                ),
                (
                    "filename_pattern",
                    models.CharField(
                        default="output.pdf",
                        help_text="Pattern for generating filenames",
                        max_length=100,
                        verbose_name="Filename Pattern",
                    ),
                ),
                (
                    "enabled",
                    models.BooleanField(
                        default=True,
                        help_text="Template is enabled",
                        verbose_name="Enabled",
                    ),
                ),
                (
                    "model_type",
                    models.CharField(
                        help_text="Target model type for template",
                        max_length=100,
                        validators=[report.validators.validate_report_model_type],
                    ),
                ),
                (
                    "filters",
                    models.CharField(
                        blank=True,
                        help_text="Template query filters (comma-separated list of key=value pairs)",
                        max_length=250,
                        validators=[report.validators.validate_filters],
                        verbose_name="Filters",
                    ),
                ),
                (
                    "template",
                    models.FileField(
                        help_text="Template file",
                        upload_to=report.models.rename_template,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["html", "htm"]
                            )
                        ],
                        verbose_name="Template",
                    ),
                ),
                (
                    "width",
                    models.FloatField(
                        default=50,
                        help_text="Label width, specified in mm",
                        validators=[django.core.validators.MinValueValidator(2)],
                        verbose_name="Width [mm]",
                    ),
                ),
                (
                    "height",
                    models.FloatField(
                        default=20,
                        help_text="Label height, specified in mm",
                        validators=[django.core.validators.MinValueValidator(2)],
                        verbose_name="Height [mm]",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("name", "model_type")},
            },
            bases=(
                report.models.TemplateUploadMixin,
                InvenTree.models.PluginValidationMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="LabelOutput",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "items",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Number of items to process",
                        verbose_name="Items",
                    ),
                ),
                (
                    "complete",
                    models.BooleanField(
                        default=False,
                        help_text="Report generation is complete",
                        verbose_name="Complete",
                    ),
                ),
                (
                    "progress",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Report generation progress",
                        verbose_name="Progress",
                    ),
                ),
                (
                    "plugin",
                    models.CharField(
                        blank=True,
                        help_text="Label output plugin",
                        max_length=100,
                        verbose_name="Plugin",
                    ),
                ),
                (
                    "output",
                    models.FileField(
                        blank=True,
                        help_text="Generated output file",
                        null=True,
                        upload_to="label/output",
                        verbose_name="Output File",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="report.labeltemplate",
                        verbose_name="Label Template",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
