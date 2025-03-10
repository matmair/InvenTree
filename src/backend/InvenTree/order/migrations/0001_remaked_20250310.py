# Generated by Django 4.2.19 on 2025-03-10 22:44

import InvenTree.fields
import InvenTree.models
import InvenTree.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import djmoney.models.validators
import generic.states.fields
import generic.states.states
import generic.states.transition
import generic.states.validators
import order.status_codes
import order.validators


class Migration(migrations.Migration):

    replaces = [('order', '0001_initial'), ('order', '0002_auto_20190604_2224'), ('order', '0003_auto_20190604_2226'), ('order', '0004_purchaseorder_status'), ('order', '0005_purchaseorderlineitem_part'), ('order', '0006_auto_20190605_2056'), ('order', '0007_auto_20190605_2138'), ('order', '0008_auto_20190605_2140'), ('order', '0009_auto_20190606_2133'), ('order', '0010_purchaseorderlineitem_notes'), ('order', '0011_auto_20190615_1928'), ('order', '0012_auto_20190617_1943'), ('order', '0013_auto_20191118_2323'), ('order', '0014_auto_20191118_2328'), ('order', '0015_auto_20200201_2346'), ('order', '0016_purchaseorderattachment'), ('order', '0017_auto_20200331_1000'), ('order', '0018_auto_20200406_0151'), ('order', '0019_purchaseorder_supplier_reference'), ('order', '0020_auto_20200420_0940'), ('order', '0021_auto_20200420_1010'), ('order', '0022_salesorderlineitem_part'), ('order', '0023_auto_20200420_2309'), ('order', '0024_salesorderallocation'), ('order', '0025_auto_20200422_0222'), ('order', '0026_auto_20200422_0224'), ('order', '0027_auto_20200422_0236'), ('order', '0028_auto_20200423_0956'), ('order', '0029_auto_20200423_1042'), ('order', '0030_auto_20200426_0551'), ('order', '0031_auto_20200426_0612'), ('order', '0032_auto_20200427_0044'), ('order', '0033_auto_20200512_1033'), ('order', '0034_auto_20200512_1054'), ('order', '0035_auto_20200513_0016'), ('order', '0036_auto_20200831_0912'), ('order', '0037_auto_20201110_0911'), ('order', '0038_auto_20201112_1737'), ('order', '0039_auto_20201112_2203'), ('order', '0040_salesorder_target_date'), ('order', '0041_auto_20210114_1728'), ('order', '0042_auto_20210310_1619'), ('order', '0043_auto_20210330_0013'), ('order', '0044_auto_20210404_2016'), ('order', '0045_auto_20210504_1946'), ('order', '0046_purchaseorderlineitem_destination'), ('order', '0047_auto_20210701_0509'), ('order', '0048_auto_20210702_2321'), ('order', '0049_alter_purchaseorderlineitem_unique_together'), ('order', '0050_alter_purchaseorderlineitem_destination'), ('order', '0051_auto_20211014_0623'), ('order', '0052_auto_20211014_0631'), ('order', '0053_auto_20211128_0151'), ('order', '0053_salesordershipment'), ('order', '0054_auto_20211201_2139'), ('order', '0054_salesorderallocation_shipment'), ('order', '0055_auto_20211025_0645'), ('order', '0056_alter_salesorderallocation_shipment'), ('order', '0057_salesorderlineitem_shipped'), ('order', '0058_auto_20211126_1210'), ('order', '0059_salesordershipment_tracking_number'), ('order', '0060_auto_20211129_1339'), ('order', '0061_merge_0054_auto_20211201_2139_0060_auto_20211129_1339'), ('order', '0062_auto_20220228_0321'), ('order', '0063_alter_purchaseorderlineitem_unique_together'), ('order', '0064_purchaseorderextraline_salesorderextraline'), ('order', '0065_alter_purchaseorderlineitem_part'), ('order', '0066_alter_purchaseorder_supplier'), ('order', '0067_auto_20220516_1120'), ('order', '0068_alter_salesorderallocation_unique_together'), ('order', '0069_auto_20220524_0508'), ('order', '0070_auto_20220620_0728'), ('order', '0071_auto_20220628_0133'), ('order', '0072_alter_salesorder_reference'), ('order', '0073_alter_purchaseorder_reference'), ('order', '0074_auto_20220709_0108'), ('order', '0075_auto_20221110_0108'), ('order', '0076_auto_20221111_0153'), ('order', '0077_auto_20230129_0154'), ('order', '0078_auto_20230304_0721'), ('order', '0079_auto_20230304_0904'), ('order', '0080_auto_20230317_0816'), ('order', '0081_auto_20230314_0725'), ('order', '0082_auto_20230314_1259'), ('order', '0083_returnorderextraline'), ('order', '0084_auto_20230321_1111'), ('order', '0085_auto_20230322_1056'), ('order', '0086_auto_20230323_1108'), ('order', '0087_alter_salesorder_status'), ('order', '0088_auto_20230403_1402'), ('order', '0089_auto_20230404_0030'), ('order', '0090_auto_20230412_1752'), ('order', '0091_auto_20230419_0037'), ('order', '0092_auto_20230419_0250'), ('order', '0093_auto_20230426_0248'), ('order', '0094_auto_20230514_2331'), ('order', '0095_salesordershipment_delivery_date'), ('order', '0096_alter_returnorderlineitem_outcome'), ('order', '0097_auto_20230529_0107'), ('order', '0098_auto_20231024_1844'), ('order', '0099_alter_salesorder_status'), ('order', '0100_remove_returnorderattachment_order_and_more'), ('order', '0101_purchaseorder_status_custom_key_and_more'), ('order', '0102_purchaseorder_destination_and_more'), ('order', '0103_alter_salesorderallocation_shipment'), ('order', '0104_alter_returnorderlineitem_quantity'), ('order', '0105_auto_20241128_0431')]

    initial = True

    dependencies = [
        ('auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('reference_int', models.BigIntegerField(default=0)),
                ('notes', InvenTree.fields.InvenTreeNotesField(blank=True, help_text='Markdown notes (optional)', max_length=50000, null=True, verbose_name='Notes')),
                ('barcode_data', models.CharField(blank=True, help_text='Third party barcode data', max_length=500, verbose_name='Barcode Data')),
                ('barcode_hash', models.CharField(blank=True, help_text='Unique hash of barcode data', max_length=128, verbose_name='Barcode Hash')),
                ('total_price_currency', djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True)),
                ('total_price', InvenTree.fields.InvenTreeModelMoneyField(blank=True, currency_choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], decimal_places=6, default_currency='USD', help_text='Total price for this order', max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Total Price')),
                ('order_currency', models.CharField(blank=True, help_text='Currency for this order (leave blank to use company default)', max_length=3, null=True, validators=[InvenTree.validators.validate_currency_code], verbose_name='Order Currency')),
                ('description', models.CharField(blank=True, help_text='Order description (optional)', max_length=250, verbose_name='Description')),
                ('link', InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external page', max_length=2000, verbose_name='Link')),
                ('start_date', models.DateField(blank=True, help_text='Scheduled start date for this order', null=True, verbose_name='Start date')),
                ('target_date', models.DateField(blank=True, help_text='Expected date for order delivery. Order will be overdue after this date.', null=True, verbose_name='Target Date')),
                ('creation_date', models.DateField(blank=True, null=True, verbose_name='Creation Date')),
                ('reference', models.CharField(default=order.validators.generate_next_purchase_order_reference, help_text='Order reference', max_length=64, unique=True, validators=[order.validators.validate_purchase_order_reference], verbose_name='Reference')),
                ('status', generic.states.fields.InvenTreeCustomStatusModelField(choices=[(10, 'Pending'), (20, 'Placed'), (25, 'On Hold'), (30, 'Complete'), (40, 'Cancelled'), (50, 'Lost'), (60, 'Returned')], default=10, help_text='Purchase order status', validators=[generic.states.validators.CustomStatusCodeValidator(status_class=order.status_codes.PurchaseOrderStatus)], verbose_name='Status')),
                ('supplier_reference', models.CharField(blank=True, help_text='Supplier order reference code', max_length=64, verbose_name='Supplier Reference')),
                ('issue_date', models.DateField(blank=True, help_text='Date order was issued', null=True, verbose_name='Issue Date')),
                ('complete_date', models.DateField(blank=True, help_text='Date order was completed', null=True, verbose_name='Completion Date')),
                ('status_custom_key', generic.states.fields.ExtraInvenTreeCustomStatusModelField(blank=True, default=None, help_text='Additional status information for this item', null=True, validators=[generic.states.validators.CustomStatusCodeValidator(status_class=order.status_codes.PurchaseOrderStatus)], verbose_name='Custom status key')),
            ],
            options={
                'verbose_name': 'Purchase Order',
            },
            bases=(generic.states.states.StatusCodeMixin, generic.states.transition.StateTransitionMixin, InvenTree.models.InvenTreeAttachmentMixin, InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PurchaseOrderExtraLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('quantity', InvenTree.fields.RoundingDecimalField(decimal_places=5, default=1, help_text='Item quantity', max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantity')),
                ('reference', models.CharField(blank=True, help_text='Line item reference', max_length=100, verbose_name='Reference')),
                ('notes', models.CharField(blank=True, help_text='Line item notes', max_length=500, verbose_name='Notes')),
                ('link', InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external page', max_length=2000, verbose_name='Link')),
                ('target_date', models.DateField(blank=True, help_text='Target date for this line item (leave blank to use the target date from the order)', null=True, verbose_name='Target Date')),
                ('description', models.CharField(blank=True, help_text='Line item description (optional)', max_length=250, verbose_name='Description')),
                ('context', models.JSONField(blank=True, help_text='Additional context for this line', null=True, verbose_name='Context')),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True)),
                ('price', InvenTree.fields.InvenTreeModelMoneyField(blank=True, currency_choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], decimal_places=6, default_currency='USD', help_text='Unit price', max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Price')),
            ],
            options={
                'verbose_name': 'Purchase Order Extra Line',
            },
            bases=(InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PurchaseOrderLineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('quantity', InvenTree.fields.RoundingDecimalField(decimal_places=5, default=1, help_text='Item quantity', max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantity')),
                ('reference', models.CharField(blank=True, help_text='Line item reference', max_length=100, verbose_name='Reference')),
                ('notes', models.CharField(blank=True, help_text='Line item notes', max_length=500, verbose_name='Notes')),
                ('link', InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external page', max_length=2000, verbose_name='Link')),
                ('target_date', models.DateField(blank=True, help_text='Target date for this line item (leave blank to use the target date from the order)', null=True, verbose_name='Target Date')),
                ('received', models.DecimalField(decimal_places=5, default=0, help_text='Number of items received', max_digits=15, verbose_name='Received')),
                ('purchase_price_currency', djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True)),
                ('purchase_price', InvenTree.fields.InvenTreeModelMoneyField(blank=True, currency_choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], decimal_places=6, default_currency='USD', help_text='Unit purchase price', max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Purchase Price')),
            ],
            options={
                'verbose_name': 'Purchase Order Line Item',
            },
            bases=(InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ReturnOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('reference_int', models.BigIntegerField(default=0)),
                ('notes', InvenTree.fields.InvenTreeNotesField(blank=True, help_text='Markdown notes (optional)', max_length=50000, null=True, verbose_name='Notes')),
                ('barcode_data', models.CharField(blank=True, help_text='Third party barcode data', max_length=500, verbose_name='Barcode Data')),
                ('barcode_hash', models.CharField(blank=True, help_text='Unique hash of barcode data', max_length=128, verbose_name='Barcode Hash')),
                ('total_price_currency', djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True)),
                ('total_price', InvenTree.fields.InvenTreeModelMoneyField(blank=True, currency_choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], decimal_places=6, default_currency='USD', help_text='Total price for this order', max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Total Price')),
                ('order_currency', models.CharField(blank=True, help_text='Currency for this order (leave blank to use company default)', max_length=3, null=True, validators=[InvenTree.validators.validate_currency_code], verbose_name='Order Currency')),
                ('description', models.CharField(blank=True, help_text='Order description (optional)', max_length=250, verbose_name='Description')),
                ('link', InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external page', max_length=2000, verbose_name='Link')),
                ('start_date', models.DateField(blank=True, help_text='Scheduled start date for this order', null=True, verbose_name='Start date')),
                ('target_date', models.DateField(blank=True, help_text='Expected date for order delivery. Order will be overdue after this date.', null=True, verbose_name='Target Date')),
                ('creation_date', models.DateField(blank=True, null=True, verbose_name='Creation Date')),
                ('reference', models.CharField(default=order.validators.generate_next_return_order_reference, help_text='Return Order reference', max_length=64, unique=True, validators=[order.validators.validate_return_order_reference], verbose_name='Reference')),
                ('status', generic.states.fields.InvenTreeCustomStatusModelField(choices=[(10, 'Pending'), (20, 'In Progress'), (25, 'On Hold'), (30, 'Complete'), (40, 'Cancelled')], default=10, help_text='Return order status', validators=[generic.states.validators.CustomStatusCodeValidator(status_class=order.status_codes.ReturnOrderStatus)], verbose_name='Status')),
                ('customer_reference', models.CharField(blank=True, help_text='Customer order reference code', max_length=64, verbose_name='Customer Reference ')),
                ('issue_date', models.DateField(blank=True, help_text='Date order was issued', null=True, verbose_name='Issue Date')),
                ('complete_date', models.DateField(blank=True, help_text='Date order was completed', null=True, verbose_name='Completion Date')),
                ('status_custom_key', generic.states.fields.ExtraInvenTreeCustomStatusModelField(blank=True, default=None, help_text='Additional status information for this item', null=True, validators=[generic.states.validators.CustomStatusCodeValidator(status_class=order.status_codes.ReturnOrderStatus)], verbose_name='Custom status key')),
            ],
            options={
                'verbose_name': 'Return Order',
            },
            bases=(generic.states.states.StatusCodeMixin, generic.states.transition.StateTransitionMixin, InvenTree.models.InvenTreeAttachmentMixin, InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ReturnOrderExtraLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('quantity', InvenTree.fields.RoundingDecimalField(decimal_places=5, default=1, help_text='Item quantity', max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantity')),
                ('reference', models.CharField(blank=True, help_text='Line item reference', max_length=100, verbose_name='Reference')),
                ('notes', models.CharField(blank=True, help_text='Line item notes', max_length=500, verbose_name='Notes')),
                ('link', InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external page', max_length=2000, verbose_name='Link')),
                ('target_date', models.DateField(blank=True, help_text='Target date for this line item (leave blank to use the target date from the order)', null=True, verbose_name='Target Date')),
                ('description', models.CharField(blank=True, help_text='Line item description (optional)', max_length=250, verbose_name='Description')),
                ('context', models.JSONField(blank=True, help_text='Additional context for this line', null=True, verbose_name='Context')),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True)),
                ('price', InvenTree.fields.InvenTreeModelMoneyField(blank=True, currency_choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], decimal_places=6, default_currency='USD', help_text='Unit price', max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Price')),
            ],
            options={
                'verbose_name': 'Return Order Extra Line',
            },
            bases=(InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ReturnOrderLineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('reference', models.CharField(blank=True, help_text='Line item reference', max_length=100, verbose_name='Reference')),
                ('notes', models.CharField(blank=True, help_text='Line item notes', max_length=500, verbose_name='Notes')),
                ('link', InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external page', max_length=2000, verbose_name='Link')),
                ('target_date', models.DateField(blank=True, help_text='Target date for this line item (leave blank to use the target date from the order)', null=True, verbose_name='Target Date')),
                ('quantity', models.DecimalField(decimal_places=5, default=1, help_text='Quantity to return', max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantity')),
                ('received_date', models.DateField(blank=True, help_text='The date this this return item was received', null=True, verbose_name='Received Date')),
                ('outcome', generic.states.fields.InvenTreeCustomStatusModelField(choices=[(10, 'Pending'), (20, 'Return'), (30, 'Repair'), (40, 'Replace'), (50, 'Refund'), (60, 'Reject')], default=10, help_text='Outcome for this line item', validators=[generic.states.validators.CustomStatusCodeValidator(status_class=order.status_codes.ReturnOrderLineStatus)], verbose_name='Outcome')),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True)),
                ('price', InvenTree.fields.InvenTreeModelMoneyField(blank=True, currency_choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], decimal_places=6, default_currency='USD', help_text='Cost associated with return or repair for this line item', max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Price')),
                ('outcome_custom_key', generic.states.fields.ExtraInvenTreeCustomStatusModelField(blank=True, default=None, help_text='Additional status information for this item', null=True, validators=[generic.states.validators.CustomStatusCodeValidator(status_class=order.status_codes.ReturnOrderLineStatus)], verbose_name='Custom status key')),
            ],
            options={
                'verbose_name': 'Return Order Line Item',
            },
            bases=(generic.states.states.StatusCodeMixin, InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('reference_int', models.BigIntegerField(default=0)),
                ('notes', InvenTree.fields.InvenTreeNotesField(blank=True, help_text='Markdown notes (optional)', max_length=50000, null=True, verbose_name='Notes')),
                ('barcode_data', models.CharField(blank=True, help_text='Third party barcode data', max_length=500, verbose_name='Barcode Data')),
                ('barcode_hash', models.CharField(blank=True, help_text='Unique hash of barcode data', max_length=128, verbose_name='Barcode Hash')),
                ('total_price_currency', djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True)),
                ('total_price', InvenTree.fields.InvenTreeModelMoneyField(blank=True, currency_choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], decimal_places=6, default_currency='USD', help_text='Total price for this order', max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Total Price')),
                ('order_currency', models.CharField(blank=True, help_text='Currency for this order (leave blank to use company default)', max_length=3, null=True, validators=[InvenTree.validators.validate_currency_code], verbose_name='Order Currency')),
                ('description', models.CharField(blank=True, help_text='Order description (optional)', max_length=250, verbose_name='Description')),
                ('link', InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external page', max_length=2000, verbose_name='Link')),
                ('start_date', models.DateField(blank=True, help_text='Scheduled start date for this order', null=True, verbose_name='Start date')),
                ('target_date', models.DateField(blank=True, help_text='Expected date for order delivery. Order will be overdue after this date.', null=True, verbose_name='Target Date')),
                ('creation_date', models.DateField(blank=True, null=True, verbose_name='Creation Date')),
                ('reference', models.CharField(default=order.validators.generate_next_sales_order_reference, help_text='Order reference', max_length=64, unique=True, validators=[order.validators.validate_sales_order_reference], verbose_name='Reference')),
                ('status', generic.states.fields.InvenTreeCustomStatusModelField(choices=[(10, 'Pending'), (15, 'In Progress'), (20, 'Shipped'), (25, 'On Hold'), (30, 'Complete'), (40, 'Cancelled'), (50, 'Lost'), (60, 'Returned')], default=10, help_text='Sales order status', validators=[generic.states.validators.CustomStatusCodeValidator(status_class=order.status_codes.SalesOrderStatus)], verbose_name='Status')),
                ('customer_reference', models.CharField(blank=True, help_text='Customer order reference code', max_length=64, verbose_name='Customer Reference ')),
                ('shipment_date', models.DateField(blank=True, null=True, verbose_name='Shipment Date')),
                ('status_custom_key', generic.states.fields.ExtraInvenTreeCustomStatusModelField(blank=True, default=None, help_text='Additional status information for this item', null=True, validators=[generic.states.validators.CustomStatusCodeValidator(status_class=order.status_codes.SalesOrderStatus)], verbose_name='Custom status key')),
            ],
            options={
                'verbose_name': 'Sales Order',
            },
            bases=(generic.states.states.StatusCodeMixin, generic.states.transition.StateTransitionMixin, InvenTree.models.InvenTreeAttachmentMixin, InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SalesOrderAllocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', InvenTree.fields.RoundingDecimalField(decimal_places=5, default=1, help_text='Enter stock allocation quantity', max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantity')),
            ],
            options={
                'verbose_name': 'Sales Order Allocation',
            },
        ),
        migrations.CreateModel(
            name='SalesOrderExtraLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('quantity', InvenTree.fields.RoundingDecimalField(decimal_places=5, default=1, help_text='Item quantity', max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantity')),
                ('reference', models.CharField(blank=True, help_text='Line item reference', max_length=100, verbose_name='Reference')),
                ('notes', models.CharField(blank=True, help_text='Line item notes', max_length=500, verbose_name='Notes')),
                ('link', InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external page', max_length=2000, verbose_name='Link')),
                ('target_date', models.DateField(blank=True, help_text='Target date for this line item (leave blank to use the target date from the order)', null=True, verbose_name='Target Date')),
                ('description', models.CharField(blank=True, help_text='Line item description (optional)', max_length=250, verbose_name='Description')),
                ('context', models.JSONField(blank=True, help_text='Additional context for this line', null=True, verbose_name='Context')),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True)),
                ('price', InvenTree.fields.InvenTreeModelMoneyField(blank=True, currency_choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], decimal_places=6, default_currency='USD', help_text='Unit price', max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Price')),
            ],
            options={
                'verbose_name': 'Sales Order Extra Line',
            },
            bases=(InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SalesOrderShipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('notes', InvenTree.fields.InvenTreeNotesField(blank=True, help_text='Markdown notes (optional)', max_length=50000, null=True, verbose_name='Notes')),
                ('shipment_date', models.DateField(blank=True, help_text='Date of shipment', null=True, verbose_name='Shipment Date')),
                ('delivery_date', models.DateField(blank=True, help_text='Date of delivery of shipment', null=True, verbose_name='Delivery Date')),
                ('reference', models.CharField(default='1', help_text='Shipment number', max_length=100, verbose_name='Shipment')),
                ('tracking_number', models.CharField(blank=True, help_text='Shipment tracking information', max_length=100, verbose_name='Tracking Number')),
                ('invoice_number', models.CharField(blank=True, help_text='Reference number for associated invoice', max_length=100, verbose_name='Invoice Number')),
                ('link', InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external page', max_length=2000, verbose_name='Link')),
                ('checked_by', models.ForeignKey(blank=True, help_text='User who checked this shipment', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Checked By')),
                ('order', models.ForeignKey(help_text='Sales Order', on_delete=django.db.models.deletion.CASCADE, related_name='shipments', to='order.salesorder', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Sales Order Shipment',
            },
            bases=(InvenTree.models.InvenTreeAttachmentMixin, InvenTree.models.PluginValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SalesOrderLineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')),
                ('quantity', InvenTree.fields.RoundingDecimalField(decimal_places=5, default=1, help_text='Item quantity', max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantity')),
                ('reference', models.CharField(blank=True, help_text='Line item reference', max_length=100, verbose_name='Reference')),
                ('notes', models.CharField(blank=True, help_text='Line item notes', max_length=500, verbose_name='Notes')),
                ('link', InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external page', max_length=2000, verbose_name='Link')),
                ('target_date', models.DateField(blank=True, help_text='Target date for this line item (leave blank to use the target date from the order)', null=True, verbose_name='Target Date')),
                ('sale_price_currency', djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True)),
                ('sale_price', InvenTree.fields.InvenTreeModelMoneyField(blank=True, currency_choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('NZD', 'New Zealand Dollar'), ('USD', 'US Dollar')], decimal_places=6, default_currency='USD', help_text='Unit sale price', max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Sale Price')),
                ('shipped', InvenTree.fields.RoundingDecimalField(decimal_places=5, default=0, help_text='Shipped quantity', max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Shipped')),
                ('order', models.ForeignKey(help_text='Sales Order', on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='order.salesorder', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Sales Order Line Item',
            },
            bases=(InvenTree.models.PluginValidationMixin, models.Model),
        ),
    ]
