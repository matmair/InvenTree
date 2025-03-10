# Generated by Django 4.2.19 on 2025-03-10 22:44

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

    replaces = [('stock', '0001_initial'), ('stock', '0002_auto_20190525_2226'), ('stock', '0003_auto_20190525_2303'), ('stock', '0004_auto_20190525_2356'), ('stock', '0005_auto_20190602_1944'), ('stock', '0006_stockitem_purchase_order'), ('stock', '0007_auto_20190618_0042'), ('stock', '0008_stockitemtracking_url'), ('stock', '0009_auto_20190715_2351'), ('stock', '0010_stockitem_build'), ('stock', '0011_auto_20190908_0404'), ('stock', '0012_auto_20190908_0405'), ('stock', '0013_auto_20190908_0916'), ('stock', '0014_auto_20190908_0918'), ('stock', '0015_auto_20190913_1407'), ('stock', '0016_auto_20191118_2146'), ('stock', '0017_auto_20191118_2311'), ('stock', '0018_auto_20200202_0103'), ('stock', '0019_auto_20200202_1024'), ('stock', '0020_auto_20200206_1213'), ('stock', '0021_auto_20200215_2232'), ('stock', '0022_auto_20200217_1109'), ('stock', '0023_auto_20200318_1027'), ('stock', '0024_auto_20200405_2239'), ('stock', '0025_auto_20200405_2243'), ('stock', '0026_stockitem_uid'), ('stock', '0027_stockitem_sales_order'), ('stock', '0028_auto_20200421_0724'), ('stock', '0029_auto_20200421_2359'), ('stock', '0030_auto_20200422_0015'), ('stock', '0031_auto_20200422_0209'), ('stock', '0032_stockitem_build_order'), ('stock', '0033_auto_20200426_0539'), ('stock', '0034_auto_20200426_0602'), ('stock', '0035_auto_20200502_2308'), ('stock', '0036_stockitemattachment'), ('stock', '0037_stockitemattachment_user'), ('stock', '0038_stockitemattachment_upload_date'), ('stock', '0039_auto_20200513_0016'), ('stock', '0040_stockitemtestresult'), ('stock', '0041_stockitemtestresult_notes'), ('stock', '0042_auto_20200523_0121'), ('stock', '0043_auto_20200525_0420'), ('stock', '0044_auto_20200528_1036'), ('stock', '0045_stockitem_customer'), ('stock', '0046_auto_20200605_0931'), ('stock', '0047_auto_20200605_0932'), ('stock', '0048_auto_20200807_2344'), ('stock', '0049_auto_20200820_0454'), ('stock', '0050_auto_20200821_1403'), ('stock', '0051_auto_20200928_0928'), ('stock', '0052_stockitem_is_building'), ('stock', '0053_auto_20201110_0513'), ('stock', '0054_remove_stockitem_build_order'), ('stock', '0055_auto_20201117_1453'), ('stock', '0056_stockitem_expiry_date'), ('stock', '0057_stock_location_item_owner'), ('stock', '0058_stockitem_packaging'), ('stock', '0059_auto_20210404_2016'), ('stock', '0060_auto_20210511_1713'), ('stock', '0061_auto_20210511_0911'), ('stock', '0062_auto_20210511_2151'), ('stock', '0063_auto_20210511_2343'), ('stock', '0064_auto_20210621_1724'), ('stock', '0065_auto_20210701_0509'), ('stock', '0066_stockitem_scheduled_for_deletion'), ('stock', '0067_alter_stockitem_part'), ('stock', '0068_stockitem_serial_int'), ('stock', '0069_auto_20211109_2347'), ('stock', '0070_auto_20211128_0151'), ('stock', '0071_auto_20211205_1733'), ('stock', '0072_remove_stockitem_scheduled_for_deletion'), ('stock', '0073_alter_stockitem_belongs_to'), ('stock', '0074_alter_stockitem_batch'), ('stock', '0075_auto_20220515_1440'), ('stock', '0076_alter_stockitem_status'), ('stock', '0077_alter_stockitem_notes'), ('stock', '0078_alter_stockitem_supplier_part'), ('stock', '0079_alter_stocklocation_name'), ('stock', '0080_stocklocation_pathstring'), ('stock', '0081_auto_20220801_0044'), ('stock', '0082_alter_stockitem_link'), ('stock', '0083_stocklocation_icon'), ('stock', '0084_auto_20220903_0154'), ('stock', '0085_auto_20220903_0225'), ('stock', '0086_remove_stockitem_uid'), ('stock', '0087_auto_20220912_2341'), ('stock', '0088_remove_stockitem_infinite'), ('stock', '0089_alter_stockitem_purchase_price'), ('stock', '0090_stocklocation_structural'), ('stock', '0091_alter_stockitem_delete_on_deplete'), ('stock', '0092_alter_stockitem_updated'), ('stock', '0093_auto_20230217_2140'), ('stock', '0094_auto_20230220_0025'), ('stock', '0095_stocklocation_external'), ('stock', '0096_auto_20230330_1121'), ('stock', '0097_alter_stockitem_notes'), ('stock', '0098_auto_20230427_2033'), ('stock', '0099_alter_stockitem_status'), ('stock', '0100_auto_20230515_0004'), ('stock', '0100_stockitem_consumed_by'), ('stock', '0101_stockitemtestresult_metadata'), ('stock', '0102_alter_stockitem_status'), ('stock', '0103_stock_location_types'), ('stock', '0104_alter_stockitem_purchase_price_currency'), ('stock', '0105_stockitemtestresult_template'), ('stock', '0106_auto_20240207_0353'), ('stock', '0107_remove_stockitemtestresult_test_and_more'), ('stock', '0108_auto_20240219_0252'), ('stock', '0109_add_additional_test_fields'), ('stock', '0110_alter_stockitemtestresult_finished_datetime_and_more'), ('stock', '0111_delete_stockitemattachment'), ('stock', '0112_alter_stocklocation_custom_icon_and_more'), ('stock', '0113_stockitem_status_custom_key_and_more'), ('stock', '0114_alter_stocklocation_custom_icon'), ('stock', '0115_auto_20250221_1323')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('notes', InvenTree.fields.InvenTreeNotesField(blank=True, help_text='Markdown notes (optional)', max_length=50000, null=True, verbose_name='Notes')),
                ('barcode_data', models.CharField(blank=True, help_text='Third party barcode data', max_length=500, verbose_name='Barcode Data')),
                ('barcode_hash', models.CharField(blank=True, help_text='Unique hash of barcode data', max_length=128, verbose_name='Barcode Hash')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Timestamp of last update', null=True, verbose_name='Updated')),
                ('packaging', models.CharField(blank=True, help_text='Packaging this stock item is stored in', max_length=50, null=True, verbose_name='Packaging')),
                ('serial', models.CharField(blank=True, help_text='Serial number for this item', max_length=100, null=True, verbose_name='Serial Number')),
                ('serial_int', models.IntegerField(default=0)),
                ('link', InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external URL', max_length=2000, verbose_name='External Link')),
                ('batch', models.CharField(blank=True, default=stock.generators.generate_batch_code, help_text='Batch code for this stock item', max_length=100, null=True, verbose_name='Batch Code')),
                ('quantity', models.DecimalField(decimal_places=5, default=1, max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Stock Quantity')),
                ('is_building', models.BooleanField(default=False)),
                ('expiry_date', models.DateField(blank=True, help_text='Expiry date for stock item. Stock will be considered expired after this date', null=True, verbose_name='Expiry Date')),
                ('stocktake_date', models.DateField(blank=True, null=True)),
                ('review_needed', models.BooleanField(default=False)),
                ('delete_on_deplete', models.BooleanField(default=stock.models.default_delete_on_deplete, help_text='Delete this Stock Item when stock is depleted', verbose_name='Delete on deplete')),
                ('status', generic.states.fields.InvenTreeCustomStatusModelField(choices=[(10, 'OK'), (50, 'Attention needed'), (55, 'Damaged'), (60, 'Destroyed'), (65, 'Rejected'), (70, 'Lost'), (75, 'Quarantined'), (85, 'Returned')], default=10, validators=[django.core.validators.MinValueValidator(0), generic.states.validators.CustomStatusCodeValidator(status_class=stock.status_codes.StockStatus)])),
                ('purchase_price_currency', djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True)),
                ('purchase_price', InvenTree.fields.InvenTreeModelMoneyField(blank=True, currency_choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], decimal_places=6, default_currency='USD', help_text='Single unit purchase price at time of purchase', max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Purchase Price')),
                ('status_custom_key', generic.states.fields.ExtraInvenTreeCustomStatusModelField(blank=True, default=None, help_text='Additional status information for this item', null=True, validators=[generic.states.validators.CustomStatusCodeValidator(status_class=stock.status_codes.StockStatus)], verbose_name='Custom status key')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Stock Item',
            },
            bases=(InvenTree.models.InvenTreeAttachmentMixin, generic.states.states.StatusCodeMixin, InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StockItemTestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('result', models.BooleanField(default=False, help_text='Test result', verbose_name='Result')),
                ('value', models.CharField(blank=True, help_text='Test output value', max_length=500, verbose_name='Value')),
                ('attachment', models.FileField(blank=True, help_text='Test result attachment', null=True, upload_to=stock.models.rename_stock_item_test_result_attachment, verbose_name='Attachment')),
                ('notes', models.CharField(blank=True, help_text='Test notes', max_length=500, verbose_name='Notes')),
                ('test_station', models.CharField(blank=True, help_text='The identifier of the test station where the test was performed', max_length=500, verbose_name='Test station')),
                ('started_datetime', models.DateTimeField(blank=True, help_text='The timestamp of the test start', null=True, verbose_name='Started')),
                ('finished_datetime', models.DateTimeField(blank=True, help_text='The timestamp of the test finish', null=True, verbose_name='Finished')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Stock Item Test Result',
            },
            bases=(InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StockItemTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_type', models.IntegerField(default=stock.status_codes.StockHistoryCode['LEGACY'])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.CharField(blank=True, help_text='Entry notes', max_length=512, null=True, verbose_name='Notes')),
                ('deltas', models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Stock Item Tracking',
            },
            bases=(InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StockLocationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('name', models.CharField(help_text='Name', max_length=100, verbose_name='Name')),
                ('description', models.CharField(blank=True, help_text='Description (optional)', max_length=250, verbose_name='Description')),
                ('icon', models.CharField(blank=True, help_text='Default icon for all locations that have no icon set (optional)', max_length=100, validators=[common.icons.validate_icon], verbose_name='Icon')),
            ],
            options={
                'verbose_name': 'Stock Location type',
                'verbose_name_plural': 'Stock Location types',
            },
        ),
        migrations.CreateModel(
            name='StockLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('name', models.CharField(help_text='Name', max_length=100, verbose_name='Name')),
                ('description', models.CharField(blank=True, help_text='Description (optional)', max_length=250, verbose_name='Description')),
                ('pathstring', models.CharField(blank=True, help_text='Path', max_length=250, verbose_name='Path')),
                ('barcode_data', models.CharField(blank=True, help_text='Third party barcode data', max_length=500, verbose_name='Barcode Data')),
                ('barcode_hash', models.CharField(blank=True, help_text='Unique hash of barcode data', max_length=128, verbose_name='Barcode Hash')),
                ('custom_icon', models.CharField(blank=True, db_column='icon', help_text='Icon (optional)', max_length=100, null=True, validators=[common.icons.validate_icon], verbose_name='Icon')),
                ('structural', models.BooleanField(default=False, help_text='Stock items may not be directly located into a structural stock locations, but may be located to child locations.', verbose_name='Structural')),
                ('external', models.BooleanField(default=False, help_text='This is an external stock location', verbose_name='External')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('location_type', models.ForeignKey(blank=True, help_text='Stock location type of this location', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_locations', to='stock.stocklocationtype', verbose_name='Location type')),
            ],
            options={
                'verbose_name': 'Stock Location',
                'verbose_name_plural': 'Stock Locations',
            },
            bases=(InvenTree.models.PluginValidationMixin, models.Model),
        ),
    ]
