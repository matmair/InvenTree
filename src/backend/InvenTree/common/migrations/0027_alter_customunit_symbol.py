# Generated by Django 4.2.12 on 2024-07-04 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0026_auto_20240608_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customunit',
            name='symbol',
            field=models.CharField(blank=True, help_text='Optional unit symbol', max_length=10, verbose_name='Symbol'),
        ),
    ]
