# Generated by Django 4.2.19 on 2025-02-21 12:30

import InvenTree.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("build", "0054_build_start_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='link',
            field=models.TextField()  # Temporary change to force new ALTER COLUMN operation in the next migration
        ),
    ]
