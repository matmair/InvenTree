# Generated by Django 3.2.19 on 2023-05-31 12:05

"""
Note: This is a total hack method to delete columns (if they already exist).

Due to an improper set of migrations merges,
there may exist a situation where the columns (defined in the migrations below) already exist.

In this case, we want to delete the columns, and then re-add them.

Original error: https://github.com/inventree/InvenTree/pull/4898
1st fix: https://github.com/inventree/InvenTree/pull/4961
2nd fix: https://github.com/inventree/InvenTree/pull/4977
3rd fix: https://github.com/inventree/InvenTree/pull/4987
"""
from ._fnc import AddFieldOrSkip, RemoveFieldOrSkip
from django.db import migrations, models


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('part', '0111_auto_20230521_1350'),
    ]

    operations = [
        RemoveFieldOrSkip(
            model_name='partparametertemplate',
            name='checkbox',
        ),
        RemoveFieldOrSkip(
            model_name='partparametertemplate',
            name='choices',
        ),
        AddFieldOrSkip(
            model_name='partparametertemplate',
            name='checkbox',
            field=models.BooleanField(default=False, help_text='Is this parameter a checkbox?', verbose_name='Checkbox'),
        ),
        AddFieldOrSkip(
            model_name='partparametertemplate',
            name='choices',
            field=models.CharField(blank=True, help_text='Valid choices for this parameter (comma-separated)', max_length=5000, verbose_name='Choices'),
        ),
    ]
