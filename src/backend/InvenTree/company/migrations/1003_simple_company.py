# Generated by Django 4.2 on 2023-06-11 11:08

import common.models
import common.settings
import django.core.validators
import django.db.models.deletion
import djmoney.models.fields
import djmoney.models.validators
import stdimage.models
import taggit.managers
from common.currency import currency_code_default
from django.conf import settings
from django.db import migrations, models

import company.models
import InvenTree.fields
import InvenTree.models
import InvenTree.validators


class Migration(migrations.Migration):

    replaces = [
        ("company", "0022_auto_20200613_1045"),
        ("company", "0023_auto_20200808_0715"),
        ("company", "0024_unique_name_email_constraint"),
        ("company", "0025_auto_20201110_1001"),
        ("company", "0026_auto_20201110_1011"),
        ("company", "0027_remove_supplierpricebreak_currency"),
        ("company", "0028_remove_supplierpricebreak_cost"),
        ("company", "0029_company_currency"),
        ("company", "0030_auto_20201112_1112"),
        ("company", "0031_auto_20210103_2215"),
        ("company", "0032_auto_20210403_1837"),
        ("company", "0033_auto_20210410_1528"),
        ("company", "0034_manufacturerpart"),
        ("company", "0035_supplierpart_update_1"),
        ("company", "0036_supplierpart_update_2"),
        ("company", "0037_supplierpart_update_3"),
        ("company", "0038_manufacturerpartparameter"),
        ("company", "0039_auto_20210701_0509"),
        ("company", "0040_alter_company_currency"),
        ("company", "0041_alter_company_options"),
        ("company", "0042_supplierpricebreak_updated"),
        ("company", "0043_manufacturerpartattachment"),
        ("company", "0044_auto_20220607_2204"),
        ("company", "0045_alter_company_notes"),
        ("company", "0046_alter_company_image"),
        ("company", "0047_supplierpart_pack_size"),
        ("company", "0048_auto_20220913_0312"),
        ("company", "0049_company_metadata"),
        ("company", "0050_alter_company_website"),
        ("company", "0051_alter_supplierpricebreak_price"),
        ("company", "0052_alter_supplierpricebreak_updated"),
        ("company", "0053_supplierpart_updated"),
        ("company", "0054_companyattachment"),
        ("company", "0055_auto_20230317_0816"),
        ("company", "0056_alter_company_notes"),
        ("company", "0057_auto_20230427_2033"),
        ("company", "0058_auto_20230515_0004"),
        ("company", "0059_supplierpart_pack_units"),
    ]

    dependencies = [
        ("part", "0060_merge_20201112_1722"),
        ("taggit", "0005_auto_20220424_2025"),
        ("part", "0045_auto_20200605_0932"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("company", "0021_remove_supplierpart_manufacturer_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="address",
            field=models.CharField(
                blank=True,
                help_text="Company address",
                max_length=200,
                verbose_name="Address",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="contact",
            field=models.CharField(
                blank=True,
                help_text="Point of contact",
                max_length=100,
                verbose_name="Contact",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="description",
            field=models.CharField(
                help_text="Description of the company",
                max_length=500,
                verbose_name="Company description",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="email",
            field=models.EmailField(
                blank=True,
                help_text="Contact email address",
                max_length=254,
                verbose_name="Email",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="name",
            field=models.CharField(
                help_text="Company name",
                max_length=100,
                unique=True,
                verbose_name="Company name",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="phone",
            field=models.CharField(
                blank=True,
                help_text="Contact phone number",
                max_length=50,
                verbose_name="Phone number",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="website",
            field=models.URLField(
                blank=True, help_text="Company website URL", verbose_name="Website"
            ),
        ),
        migrations.AlterModelOptions(
            name="company",
            options={"ordering": ["name"]},
        ),
        migrations.AlterField(
            model_name="company",
            name="email",
            field=models.EmailField(
                blank=True,
                help_text="Contact email address",
                max_length=254,
                null=True,
                verbose_name="Email",
            ),
        ),
        migrations.AlterField(
            model_name="supplierpart",
            name="part",
            field=models.ForeignKey(
                help_text="Select part",
                limit_choices_to={"is_template": False, "purchaseable": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="supplier_parts",
                to="part.part",
                verbose_name="Base Part",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="name",
            field=models.CharField(
                help_text="Company name", max_length=100, verbose_name="Company name"
            ),
        ),
        migrations.AddConstraint(
            model_name="company",
            constraint=models.UniqueConstraint(
                fields=("name", "email"), name="unique_name_email_pair"
            ),
        ),
        migrations.RemoveField(
            model_name="supplierpricebreak",
            name="currency",
        ),
        migrations.RemoveField(
            model_name="supplierpricebreak",
            name="cost",
        ),
        migrations.AddField(
            model_name="company",
            name="currency",
            field=models.CharField(
                blank=True,
                default=currency_code_default,
                help_text="Default currency used for this company",
                max_length=3,
                validators=[InvenTree.validators.validate_currency_code],
                verbose_name="Currency",
            ),
        ),
        migrations.AlterField(
            model_name="supplierpricebreak",
            name="quantity",
            field=InvenTree.fields.RoundingDecimalField(
                decimal_places=5,
                default=1,
                help_text="Price break quantity",
                max_digits=15,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Quantity",
            ),
        ),
        migrations.RemoveField(
            model_name="supplierpart",
            name="MPN",
        ),
        migrations.AlterField(
            model_name="supplierpart",
            name="SKU",
            field=models.CharField(
                help_text="Supplier stock keeping unit",
                max_length=100,
                verbose_name="SKU",
            ),
        ),
        migrations.AlterField(
            model_name="supplierpart",
            name="description",
            field=models.CharField(
                blank=True,
                help_text="Supplier part description",
                max_length=250,
                null=True,
                verbose_name="Description",
            ),
        ),
        migrations.AlterField(
            model_name="supplierpart",
            name="link",
            field=InvenTree.fields.InvenTreeURLField(
                blank=True,
                help_text="URL for external supplier part link",
                null=True,
                verbose_name="Link",
            ),
        ),
        migrations.RemoveField(
            model_name="supplierpart",
            name="manufacturer",
        ),
        migrations.AlterField(
            model_name="supplierpart",
            name="note",
            field=models.CharField(
                blank=True,
                help_text="Notes",
                max_length=100,
                null=True,
                verbose_name="Note",
            ),
        ),
        migrations.AlterField(
            model_name="supplierpart",
            name="packaging",
            field=models.CharField(
                blank=True, help_text="Part packaging", max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="supplierpart",
            name="part",
            field=models.ForeignKey(
                help_text="Select part",
                limit_choices_to={"purchaseable": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="supplier_parts",
                to="part.part",
                verbose_name="Base Part",
            ),
        ),
        migrations.AlterField(
            model_name="supplierpart",
            name="supplier",
            field=models.ForeignKey(
                help_text="Select supplier",
                limit_choices_to={"is_supplier": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="supplied_parts",
                to="company.company",
                verbose_name="Supplier",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="image",
            field=stdimage.models.StdImageField(
                blank=True,
                null=True,
                upload_to=company.models.rename_company_image,
                verbose_name="Image",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="is_customer",
            field=models.BooleanField(
                default=False,
                help_text="Do you sell items to this company?",
                verbose_name="is customer",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="is_manufacturer",
            field=models.BooleanField(
                default=False,
                help_text="Does this company manufacture parts?",
                verbose_name="is manufacturer",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="is_supplier",
            field=models.BooleanField(
                default=True,
                help_text="Do you purchase items from this company?",
                verbose_name="is supplier",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="link",
            field=InvenTree.fields.InvenTreeURLField(
                blank=True,
                help_text="Link to external company information",
                verbose_name="Link",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="notes",
            field=models.TextField(blank=True, verbose_name="Notes"),
        ),
        migrations.AlterField(
            model_name="supplierpart",
            name="base_cost",
            field=models.DecimalField(
                decimal_places=3,
                default=0,
                help_text="Minimum charge (e.g. stocking fee)",
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="base cost",
            ),
        ),
        migrations.AlterField(
            model_name="supplierpart",
            name="multiple",
            field=models.PositiveIntegerField(
                default=1,
                help_text="Order multiple",
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="multiple",
            ),
        ),
        migrations.AlterField(
            model_name="supplierpart",
            name="packaging",
            field=models.CharField(
                blank=True,
                help_text="Part packaging",
                max_length=50,
                null=True,
                verbose_name="Packaging",
            ),
        ),
        migrations.AlterField(
            model_name="supplierpricebreak",
            name="part",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pricebreaks",
                to="company.supplierpart",
                verbose_name="Part",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="description",
            field=models.CharField(
                blank=True,
                help_text="Description of the company",
                max_length=500,
                verbose_name="Company description",
            ),
        ),
        migrations.CreateModel(
            name="ManufacturerPart",
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
                    "MPN",
                    models.CharField(
                        help_text="Manufacturer Part Number",
                        max_length=100,
                        null=True,
                        verbose_name="MPN",
                    ),
                ),
                (
                    "link",
                    InvenTree.fields.InvenTreeURLField(
                        blank=True,
                        help_text="URL for external manufacturer part link",
                        null=True,
                        verbose_name="Link",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="Manufacturer part description",
                        max_length=250,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "manufacturer",
                    models.ForeignKey(
                        help_text="Select manufacturer",
                        limit_choices_to={"is_manufacturer": True},
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="manufactured_parts",
                        to="company.company",
                        verbose_name="Manufacturer",
                    ),
                ),
                (
                    "part",
                    models.ForeignKey(
                        help_text="Select part",
                        limit_choices_to={"purchaseable": True},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="manufacturer_parts",
                        to="part.part",
                        verbose_name="Base Part",
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
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
            options={
                "unique_together": {("part", "manufacturer", "MPN")},
            },
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="manufacturer_part",
            field=models.ForeignKey(
                blank=True,
                help_text="Select manufacturer part",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="supplier_parts",
                to="company.manufacturerpart",
                verbose_name="Manufacturer Part",
            ),
        ),
        migrations.CreateModel(
            name="ManufacturerPartParameter",
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
                    "name",
                    models.CharField(
                        help_text="Parameter name", max_length=500, verbose_name="Name"
                    ),
                ),
                (
                    "value",
                    models.CharField(
                        help_text="Parameter value",
                        max_length=500,
                        verbose_name="Value",
                    ),
                ),
                (
                    "units",
                    models.CharField(
                        blank=True,
                        help_text="Parameter units",
                        max_length=64,
                        null=True,
                        verbose_name="Units",
                    ),
                ),
                (
                    "manufacturer_part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parameters",
                        to="company.manufacturerpart",
                        verbose_name="Manufacturer Part",
                    ),
                ),
            ],
            options={
                "unique_together": {("manufacturer_part", "name")},
            },
        ),
        migrations.AddField(
            model_name="supplierpricebreak",
            name="price_currency",
            field=djmoney.models.fields.CurrencyField(
                choices=[], default="", editable=False, max_length=3
            ),
        ),
        migrations.AlterModelOptions(
            name="company",
            options={"ordering": ["name"], "verbose_name_plural": "Companies"},
        ),
        migrations.CreateModel(
            name="ManufacturerPartAttachment",
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
                    "attachment",
                    models.FileField(
                        blank=True,
                        help_text="Select file to attach",
                        null=True,
                        upload_to=common.models.rename_attachment,
                        verbose_name="Attachment",
                    ),
                ),
                (
                    "link",
                    InvenTree.fields.InvenTreeURLField(
                        blank=True,
                        help_text="Link to external URL",
                        null=True,
                        verbose_name="Link",
                    ),
                ),
                (
                    "comment",
                    models.CharField(
                        blank=True,
                        help_text="File comment",
                        max_length=100,
                        verbose_name="Comment",
                    ),
                ),
                (
                    "upload_date",
                    models.DateField(
                        auto_now_add=True, null=True, verbose_name="upload date"
                    ),
                ),
                (
                    "manufacturer_part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="company.manufacturerpart",
                        verbose_name="Manufacturer Part",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        help_text="User",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="availability_updated",
            field=models.DateTimeField(
                blank=True,
                help_text="Date of last update of availability data",
                null=True,
                verbose_name="Availability Updated",
            ),
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="available",
            field=models.DecimalField(
                decimal_places=3,
                default=0,
                help_text="Quantity available from supplier",
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Available",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="notes",
            field=InvenTree.fields.InvenTreeNotesField(
                blank=True,
                help_text="Company Notes",
                max_length=50000,
                null=True,
                verbose_name="Notes",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="image",
            field=stdimage.models.StdImageField(
                blank=True,
                null=True,
                upload_to=company.models.rename_company_image,
                verbose_name="Image",
            ),
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="pack_size",
            field=InvenTree.fields.RoundingDecimalField(
                decimal_places=5,
                default=1,
                help_text="Unit quantity supplied in a single pack",
                max_digits=15,
                validators=[django.core.validators.MinValueValidator(0.001)],
                verbose_name="Pack Quantity",
            ),
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="barcode_data",
            field=models.CharField(
                blank=True,
                help_text="Third party barcode data",
                max_length=500,
                verbose_name="Barcode Data",
            ),
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="barcode_hash",
            field=models.CharField(
                blank=True,
                help_text="Unique hash of barcode data",
                max_length=128,
                verbose_name="Barcode Hash",
            ),
        ),
        migrations.AddField(
            model_name="company",
            name="metadata",
            field=models.JSONField(
                blank=True,
                help_text="JSON metadata field, for use by external plugins",
                null=True,
                verbose_name="Plugin Metadata",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="website",
            field=InvenTree.fields.InvenTreeURLField(
                blank=True, help_text="Company website URL", verbose_name="Website"
            ),
        ),
        migrations.AddField(
            model_name="supplierpricebreak",
            name="price",
            field=InvenTree.fields.InvenTreeModelMoneyField(
                decimal_places=6,
                default_currency="EUR",
                help_text="Unit price at specified quantity",
                max_digits=19,
                null=True,
                validators=[djmoney.models.validators.MinMoneyValidator(0)],
                verbose_name="Price",
            ),
        ),
        migrations.AddField(
            model_name="supplierpricebreak",
            name="updated",
            field=models.DateTimeField(
                auto_now=True,
                help_text="Timestamp of last update",
                null=True,
                verbose_name="Updated",
            ),
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="updated",
            field=models.DateTimeField(
                auto_now=True,
                help_text="Timestamp of last update",
                null=True,
                verbose_name="Updated",
            ),
        ),
        migrations.CreateModel(
            name="CompanyAttachment",
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
                    "attachment",
                    models.FileField(
                        blank=True,
                        help_text="Select file to attach",
                        null=True,
                        upload_to=common.models.rename_attachment,
                        verbose_name="Attachment",
                    ),
                ),
                (
                    "link",
                    InvenTree.fields.InvenTreeURLField(
                        blank=True,
                        help_text="Link to external URL",
                        null=True,
                        verbose_name="Link",
                    ),
                ),
                (
                    "comment",
                    models.CharField(
                        blank=True,
                        help_text="File comment",
                        max_length=100,
                        verbose_name="Comment",
                    ),
                ),
                (
                    "upload_date",
                    models.DateField(
                        auto_now_add=True, null=True, verbose_name="upload date"
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="company.company",
                        verbose_name="Company",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        help_text="User",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="metadata",
            field=models.JSONField(
                blank=True,
                help_text="JSON metadata field, for use by external plugins",
                null=True,
                verbose_name="Plugin Metadata",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="notes",
            field=InvenTree.fields.InvenTreeNotesField(
                blank=True,
                help_text="Markdown notes (optional)",
                max_length=50000,
                null=True,
                verbose_name="Notes",
            ),
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="pack_quantity",
            field=models.CharField(
                blank=True,
                help_text="Total quantity supplied in a single pack. Leave empty for single items.",
                max_length=25,
                verbose_name="Pack Quantity",
            ),
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="pack_quantity_native",
            field=InvenTree.fields.RoundingDecimalField(
                decimal_places=10, default=1, max_digits=20, null=True
            ),
        ),
    ]
