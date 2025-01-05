# Generated by Django 4.2.17 on 2025-01-05 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_squashed"),
        ("build", "0003_squashed"),
        ("stock", "0001_squashed"),
        ("order", "0003_squashed"),
    ]

    operations = [
        migrations.AddField(
            model_name="build",
            name="responsible",
            field=models.ForeignKey(
                blank=True,
                help_text="User or group responsible for this build order",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="builds_responsible",
                to="users.owner",
                verbose_name="Responsible",
            ),
        ),
        migrations.AddField(
            model_name="build",
            name="sales_order",
            field=models.ForeignKey(
                blank=True,
                help_text="SalesOrder to which this build is allocated",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="builds",
                to="order.salesorder",
                verbose_name="Sales Order Reference",
            ),
        ),
        migrations.AddField(
            model_name="build",
            name="take_from",
            field=models.ForeignKey(
                blank=True,
                help_text="Select location to take stock from for this build (leave blank to take from any stock location)",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sourcing_builds",
                to="stock.stocklocation",
                verbose_name="Source Location",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="buildline",
            unique_together={("build", "bom_item")},
        ),
        migrations.AlterUniqueTogether(
            name="builditem",
            unique_together={("build_line", "stock_item", "install_into")},
        ),
    ]
