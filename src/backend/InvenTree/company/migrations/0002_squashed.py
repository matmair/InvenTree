# Generated by Django 4.2.17 on 2025-01-05 12:47

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("part", "0001_squashed"),
        ("company", "0001_squashed"),
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="supplierpart",
            name="part",
            field=models.ForeignKey(
                help_text="Select part",
                limit_choices_to={"purchaseable": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="supplier_parts",
                to="part.part",
                verbose_name="Base Part",
            ),
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="supplier",
            field=models.ForeignKey(
                help_text="Select supplier",
                limit_choices_to={"is_supplier": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="supplied_parts",
                to="company.company",
                verbose_name="Supplier",
            ),
        ),
        migrations.AddField(
            model_name="supplierpart",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="manufacturerpartparameter",
            name="manufacturer_part",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="parameters",
                to="company.manufacturerpart",
                verbose_name="Manufacturer Part",
            ),
        ),
        migrations.AddField(
            model_name="manufacturerpart",
            name="manufacturer",
            field=models.ForeignKey(
                help_text="Select manufacturer",
                limit_choices_to={"is_manufacturer": True},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="manufactured_parts",
                to="company.company",
                verbose_name="Manufacturer",
            ),
        ),
        migrations.AddField(
            model_name="manufacturerpart",
            name="part",
            field=models.ForeignKey(
                help_text="Select part",
                limit_choices_to={"purchaseable": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="manufacturer_parts",
                to="part.part",
                verbose_name="Base Part",
            ),
        ),
        migrations.AddField(
            model_name="manufacturerpart",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contacts",
                to="company.company",
            ),
        ),
        migrations.AddConstraint(
            model_name="company",
            constraint=models.UniqueConstraint(
                fields=("name", "email"), name="unique_name_email_pair"
            ),
        ),
        migrations.AddField(
            model_name="address",
            name="company",
            field=models.ForeignKey(
                help_text="Select company",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="addresses",
                to="company.company",
                verbose_name="Company",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="supplierpricebreak",
            unique_together={("part", "quantity")},
        ),
        migrations.AlterUniqueTogether(
            name="supplierpart",
            unique_together={("part", "supplier", "SKU")},
        ),
        migrations.AlterUniqueTogether(
            name="manufacturerpartparameter",
            unique_together={("manufacturer_part", "name")},
        ),
        migrations.AlterUniqueTogether(
            name="manufacturerpart",
            unique_together={("part", "manufacturer", "MPN")},
        ),
    ]
