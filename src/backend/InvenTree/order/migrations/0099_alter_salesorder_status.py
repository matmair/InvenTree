# Generated by Django 4.2.11 on 2024-04-03 00:40

import django.core.validators
from django.db import migrations, models
import InvenTree.status_codes


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0098_auto_20231024_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesorder',
            name='status',
            field=models.PositiveIntegerField(choices=InvenTree.status_codes.SalesOrderStatus.items(), default=10, help_text='Purchase order status', verbose_name='Status'),
        ),
    ]
