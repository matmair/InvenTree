# Generated by Django 4.2.17 on 2025-01-05 12:47

import InvenTree.fields
import InvenTree.models
import common.icons
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import djmoney.models.validators
import generic.states.fields
import generic.states.states
import generic.states.validators
import stock.generators
import stock.models
import stock.status_codes


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StockItem",
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
                    "notes",
                    InvenTree.fields.InvenTreeNotesField(
                        blank=True,
                        help_text="Markdown notes (optional)",
                        max_length=50000,
                        null=True,
                        verbose_name="Notes",
                    ),
                ),
                (
                    "barcode_data",
                    models.CharField(
                        blank=True,
                        help_text="Third party barcode data",
                        max_length=500,
                        verbose_name="Barcode Data",
                    ),
                ),
                (
                    "barcode_hash",
                    models.CharField(
                        blank=True,
                        help_text="Unique hash of barcode data",
                        max_length=128,
                        verbose_name="Barcode Hash",
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Timestamp of last update",
                        null=True,
                        verbose_name="Updated",
                    ),
                ),
                (
                    "packaging",
                    models.CharField(
                        blank=True,
                        help_text="Packaging this stock item is stored in",
                        max_length=50,
                        null=True,
                        verbose_name="Packaging",
                    ),
                ),
                (
                    "serial",
                    models.CharField(
                        blank=True,
                        help_text="Serial number for this item",
                        max_length=100,
                        null=True,
                        verbose_name="Serial Number",
                    ),
                ),
                ("serial_int", models.IntegerField(default=0)),
                (
                    "link",
                    InvenTree.fields.InvenTreeURLField(
                        blank=True,
                        help_text="Link to external URL",
                        verbose_name="External Link",
                    ),
                ),
                (
                    "batch",
                    models.CharField(
                        blank=True,
                        default=stock.generators.generate_batch_code,
                        help_text="Batch code for this stock item",
                        max_length=100,
                        null=True,
                        verbose_name="Batch Code",
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        decimal_places=5,
                        default=1,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Stock Quantity",
                    ),
                ),
                ("is_building", models.BooleanField(default=False)),
                (
                    "expiry_date",
                    models.DateField(
                        blank=True,
                        help_text="Expiry date for stock item. Stock will be considered expired after this date",
                        null=True,
                        verbose_name="Expiry Date",
                    ),
                ),
                ("stocktake_date", models.DateField(blank=True, null=True)),
                ("review_needed", models.BooleanField(default=False)),
                (
                    "delete_on_deplete",
                    models.BooleanField(
                        default=stock.models.default_delete_on_deplete,
                        help_text="Delete this Stock Item when stock is depleted",
                        verbose_name="Delete on deplete",
                    ),
                ),
                (
                    "status_custom_key",
                    generic.states.fields.ExtraInvenTreeCustomStatusModelField(
                        blank=True,
                        default=None,
                        help_text="Additional status information for this item",
                        null=True,
                        validators=[
                            generic.states.validators.CustomStatusCodeValidator(
                                status_class=stock.status_codes.StockStatus
                            )
                        ],
                        verbose_name="Custom status key",
                    ),
                ),
                (
                    "status",
                    generic.states.fields.InvenTreeCustomStatusModelField(
                        choices=[
                            (10, "OK"),
                            (50, "Attention needed"),
                            (55, "Damaged"),
                            (60, "Destroyed"),
                            (65, "Rejected"),
                            (70, "Lost"),
                            (75, "Quarantined"),
                            (85, "Returned"),
                        ],
                        default=10,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            generic.states.validators.CustomStatusCodeValidator(
                                status_class=stock.status_codes.StockStatus
                            ),
                        ],
                    ),
                ),
                (
                    "purchase_price_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[], default="", editable=False, max_length=3, null=True
                    ),
                ),
                (
                    "purchase_price",
                    InvenTree.fields.InvenTreeModelMoneyField(
                        blank=True,
                        currency_choices=[],
                        decimal_places=6,
                        default_currency="",
                        help_text="Single unit purchase price at time of purchase",
                        max_digits=19,
                        null=True,
                        validators=[djmoney.models.validators.MinMoneyValidator(0)],
                        verbose_name="Purchase Price",
                    ),
                ),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
            ],
            options={
                "verbose_name": "Stock Item",
            },
            bases=(
                InvenTree.models.InvenTreeAttachmentMixin,
                generic.states.states.StatusCodeMixin,
                InvenTree.models.PluginValidationMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="StockItemTestResult",
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
                    "result",
                    models.BooleanField(
                        default=False, help_text="Test result", verbose_name="Result"
                    ),
                ),
                (
                    "value",
                    models.CharField(
                        blank=True,
                        help_text="Test output value",
                        max_length=500,
                        verbose_name="Value",
                    ),
                ),
                (
                    "attachment",
                    models.FileField(
                        blank=True,
                        help_text="Test result attachment",
                        null=True,
                        upload_to=stock.models.rename_stock_item_test_result_attachment,
                        verbose_name="Attachment",
                    ),
                ),
                (
                    "notes",
                    models.CharField(
                        blank=True,
                        help_text="Test notes",
                        max_length=500,
                        verbose_name="Notes",
                    ),
                ),
                (
                    "test_station",
                    models.CharField(
                        blank=True,
                        help_text="The identifier of the test station where the test was performed",
                        max_length=500,
                        verbose_name="Test station",
                    ),
                ),
                (
                    "started_datetime",
                    models.DateTimeField(
                        blank=True,
                        help_text="The timestamp of the test start",
                        null=True,
                        verbose_name="Started",
                    ),
                ),
                (
                    "finished_datetime",
                    models.DateTimeField(
                        blank=True,
                        help_text="The timestamp of the test finish",
                        null=True,
                        verbose_name="Finished",
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Stock Item Test Result",
            },
            bases=(InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name="StockItemTracking",
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
                    "tracking_type",
                    models.IntegerField(
                        default=stock.status_codes.StockHistoryCode["LEGACY"]
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "notes",
                    models.CharField(
                        blank=True,
                        help_text="Entry notes",
                        max_length=512,
                        null=True,
                        verbose_name="Notes",
                    ),
                ),
                ("deltas", models.JSONField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Stock Item Tracking",
            },
            bases=(InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name="StockLocationType",
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
                        help_text="Name", max_length=100, verbose_name="Name"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="Description (optional)",
                        max_length=250,
                        verbose_name="Description",
                    ),
                ),
                (
                    "icon",
                    models.CharField(
                        blank=True,
                        help_text="Default icon for all locations that have no icon set (optional)",
                        max_length=100,
                        validators=[common.icons.validate_icon],
                        verbose_name="Icon",
                    ),
                ),
            ],
            options={
                "verbose_name": "Stock Location type",
                "verbose_name_plural": "Stock Location types",
            },
        ),
        migrations.CreateModel(
            name="StockLocation",
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
                        help_text="Name", max_length=100, verbose_name="Name"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="Description (optional)",
                        max_length=250,
                        verbose_name="Description",
                    ),
                ),
                (
                    "pathstring",
                    models.CharField(
                        blank=True,
                        help_text="Path",
                        max_length=250,
                        verbose_name="Path",
                    ),
                ),
                (
                    "barcode_data",
                    models.CharField(
                        blank=True,
                        help_text="Third party barcode data",
                        max_length=500,
                        verbose_name="Barcode Data",
                    ),
                ),
                (
                    "barcode_hash",
                    models.CharField(
                        blank=True,
                        help_text="Unique hash of barcode data",
                        max_length=128,
                        verbose_name="Barcode Hash",
                    ),
                ),
                (
                    "custom_icon",
                    models.CharField(
                        blank=True,
                        db_column="icon",
                        help_text="Icon (optional)",
                        max_length=100,
                        validators=[common.icons.validate_icon],
                        verbose_name="Icon",
                    ),
                ),
                (
                    "structural",
                    models.BooleanField(
                        default=False,
                        help_text="Stock items may not be directly located into a structural stock locations, but may be located to child locations.",
                        verbose_name="Structural",
                    ),
                ),
                (
                    "external",
                    models.BooleanField(
                        default=False,
                        help_text="This is an external stock location",
                        verbose_name="External",
                    ),
                ),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "location_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="Stock location type of this location",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="stock_locations",
                        to="stock.stocklocationtype",
                        verbose_name="Location type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Stock Location",
                "verbose_name_plural": "Stock Locations",
            },
            bases=(InvenTree.models.PluginValidationMixin, models.Model),
        ),
    ]
