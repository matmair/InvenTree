# Generated by Django 3.2.18 on 2023-03-14 10:07

from django.db import migrations, models
from users.ruleset import RULESET_CHOICES


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_ruleset_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ruleset',
            name='name',
            field=models.CharField(choices=RULESET_CHOICES, help_text='Permission set', max_length=50),
        ),
    ]
