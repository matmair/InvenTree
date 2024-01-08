# Generated by Django 2.2.5 on 2019-09-08 04:05

from django.db import migrations


def update_tree(apps, schema_editor):
    # Update the StockLocation MPTT model

    StockLocation = apps.get_model('stock', 'StockLocation')
    try:
        print("Rebuilding StockLocation objects")
        StockLocation.objects.rebuild()
        print("Rebuilding StockLocation objects - done")
    except Exception as exc:
        print("Error rebuilding StockLocation objects", exc)


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('stock', '0011_auto_20190908_0404'),
    ]

    operations = [
        migrations.RunPython(update_tree)
    ]
