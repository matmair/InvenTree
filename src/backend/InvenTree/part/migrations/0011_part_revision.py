# Generated by Django 2.2.2 on 2019-06-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0010_auto_20190620_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='revision',
            field=models.CharField(blank=True, help_text='Part revision or version number', max_length=100),
        ),
    ]
