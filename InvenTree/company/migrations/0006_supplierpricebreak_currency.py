# Generated by Django 2.2.4 on 2019-09-02 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        #('common', '0003_auto_20190902_2310'),
        ('company', '0005_auto_20190525_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierpricebreak',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Currency'),
        ),
    ]
