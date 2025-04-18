# Generated by Django 4.2.19 on 2025-02-21 13:46

import InvenTree.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0134_auto_20250221_1309"),
    ]

    operations = [
        migrations.AlterField(
            model_name="part",
            name="link",
            field=InvenTree.fields.InvenTreeURLField(
                blank=True,
                help_text="Link to external URL",
                max_length=2000,
                null=True,
                verbose_name="Link",
            ),
        ),
    ]
