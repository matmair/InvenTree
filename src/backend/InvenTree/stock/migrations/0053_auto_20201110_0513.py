# Generated by Django 3.0.7 on 2020-11-10 05:13

from django.db import migrations
import djmoney.models.fields
import common.currency


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_inventreesetting'),
        ('stock', '0052_stockitem_is_building'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockitem',
            name='purchase_price',
            field=djmoney.models.fields.MoneyField(decimal_places=4, default_currency=common.currency.currency_code_default(), help_text='Single unit purchase price at time of purchase', max_digits=19, null=True, verbose_name='Purchase Price'),
        ),
        migrations.AddField(
            model_name='stockitem',
            name='purchase_price_currency',
            field=djmoney.models.fields.CurrencyField(choices=common.currency.all_currency_codes(), default=common.currency.currency_code_default(), editable=False, max_length=3),
        ),
    ]
