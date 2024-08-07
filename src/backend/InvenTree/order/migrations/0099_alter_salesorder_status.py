# Generated by Django 4.2.11 on 2024-04-03 00:40

import django.core.validators
from django.db import migrations, models
import order.status_codes


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0098_auto_20231024_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesorder',
            name='status',
            field=models.PositiveIntegerField(
                choices=order.status_codes.SalesOrderStatus.items(),
                default=order.status_codes.SalesOrderStatus.PENDING.value,
                help_text='Sales order status', verbose_name='Status'
            ),
        ),
    ]
