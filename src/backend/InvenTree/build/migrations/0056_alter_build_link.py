# Generated by Django 4.2.19 on 2025-02-21 13:46

import InvenTree.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("build", "0055_auto_20250221_1230"),
    ]

    operations = [
        migrations.AlterField(
            model_name="build",
            name="link",
            field=InvenTree.fields.InvenTreeURLField(
                blank=True,
                help_text="Link to external URL",
                max_length=2000,
                verbose_name="External Link",
            ),
        ),
    ]
