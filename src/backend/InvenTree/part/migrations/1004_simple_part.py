# Generated by Django 4.2.17 on 2025-01-05 01:29

import common.icons
import django.db.migrations.operations.special
import django.db.models.deletion
from django.db import migrations, models


def set_testable(apps, schema_editor):
    """Set the 'testable' status to True for certain parts.

    Prior to migration part.0128, the 'trackable' attribute
    was used to determine if parts could have tests associated with them.

    However, 'trackable' comes with other restrictions
    (such as requiring a unique serial number).

    So, we have added a new field 'testable' to the Part model,
    which is updated in this migration to match the value of the 'trackable' field.
    """

    Part = apps.get_model("part", "Part")

    # By default, 'testable' is False - so we only need to update parts marked as 'trackable'
    trackable_parts = Part.objects.filter(trackable=True)

    if trackable_parts.count() > 0:
        print(f"\nMarking {trackable_parts.count()} Part objects as 'testable'")
        trackable_parts.update(testable=True)


class Migration(migrations.Migration):
    replaces = [
        ("part", "0124_delete_partattachment"),
        ("part", "0125_part_locked"),
        ("part", "0126_part_revision_of"),
        ("part", "0127_remove_partcategory_icon_partcategory__icon"),
        ("part", "0128_part_testable"),
        ("part", "0129_auto_20240815_0214"),
        ("part", "0130_alter_parttesttemplate_part"),
        ("part", "0131_partrelated_note"),
        ("part", "0132_partparametertemplate_selectionlist"),
    ]

    dependencies = [
        ("stock", "0110_alter_stockitemtestresult_finished_datetime_and_more"),
        ("common", "0026_auto_20240608_1238"),
        ("order", "0099_alter_salesorder_status"),
        ("company", "0069_company_active"),
        ("common", "0032_selectionlist_selectionlistentry_and_more"),
        ("part", "0123_parttesttemplate_choices"),
        ("build", "0050_auto_20240508_0138"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PartAttachment",
        ),
        migrations.AddField(
            model_name="part",
            name="locked",
            field=models.BooleanField(
                default=False,
                help_text="Locked parts cannot be edited",
                verbose_name="Locked",
            ),
        ),
        migrations.AddField(
            model_name="part",
            name="revision_of",
            field=models.ForeignKey(
                blank=True,
                help_text="Is this part a revision of another part?",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="revisions",
                to="part.part",
                verbose_name="Revision Of",
            ),
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameField(
                    model_name="partcategory",
                    old_name="icon",
                    new_name="_icon",
                ),
                migrations.AlterField(
                    model_name="partcategory",
                    name="_icon",
                    field=models.CharField(
                        blank=True,
                        db_column="icon",
                        help_text="Icon (optional)",
                        max_length=100,
                        validators=[common.icons.validate_icon],
                        verbose_name="Icon",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="part",
            name="testable",
            field=models.BooleanField(
                default=False,
                help_text="Can this part have test results recorded against it?",
                verbose_name="Testable",
            ),
        ),
        migrations.RunPython(
            code=set_testable,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="parttesttemplate",
            name="part",
            field=models.ForeignKey(
                limit_choices_to={"testable": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="test_templates",
                to="part.part",
                verbose_name="Part",
            ),
        ),
        migrations.AddField(
            model_name="partrelated",
            name="note",
            field=models.CharField(
                blank=True,
                help_text="Note for this relationship",
                max_length=500,
                verbose_name="Note",
            ),
        ),
        migrations.AddField(
            model_name="partparametertemplate",
            name="selectionlist",
            field=models.ForeignKey(
                blank=True,
                help_text="Selection list for this parameter",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="parameter_templates",
                to="common.selectionlist",
                verbose_name="Selection List",
            ),
        ),
        migrations.AlterModelOptions(
            name="partcategoryparametertemplate",
            options={"verbose_name": "Part Category Parameter Template"},
        ),
        migrations.AlterModelOptions(
            name="partparameter",
            options={"verbose_name": "Part Parameter"},
        ),
        migrations.AlterModelOptions(
            name="partparametertemplate",
            options={"verbose_name": "Part Parameter Template"},
        ),
        migrations.AlterModelOptions(
            name="partsellpricebreak",
            options={"verbose_name": "Part Sale Price Break"},
        ),
        migrations.AlterModelOptions(
            name="parttesttemplate",
            options={"verbose_name": "Part Test Template"},
        ),
    ]
