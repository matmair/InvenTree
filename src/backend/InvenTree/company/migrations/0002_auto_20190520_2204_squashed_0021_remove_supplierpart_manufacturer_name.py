import InvenTree.fields
import company.models
import django.core.validators
import django.db.models.deletion
import stdimage.models
from django.db import migrations, models
import importlib

def get_migration_func(migration_name, func_name):
    try:
        mod = importlib.import_module(f'company.migrations.{migration_name}')
        return getattr(mod, func_name)
    except (ImportError, AttributeError):
        return lambda apps, schema_editor: None

class RemoveFieldOrSkip(migrations.RemoveField):

    def database_backwards(self, app_label, schema_editor, from_state, to_state) -> None:
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state) -> None:
        try:
            super().database_forwards(app_label, schema_editor, from_state, to_state)
        except Exception:
            pass

    def state_forwards(self, app_label, state) -> None:
        try:
            super().state_forwards(app_label, state)
        except Exception:
            pass

class AddFieldOrSkip(migrations.AddField):

    def database_backwards(self, app_label, schema_editor, from_state, to_state) -> None:
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state) -> None:
        try:
            super().database_forwards(app_label, schema_editor, from_state, to_state)
        except Exception:
            pass

    def state_forwards(self, app_label, state) -> None:
        try:
            super().state_forwards(app_label, state)
        except Exception:
            pass

class Migration(migrations.Migration):
    replaces = [('company', '0002_auto_20190520_2204'), ('company', '0003_remove_supplierpart_minimum'), ('company', '0004_auto_20190525_2354'), ('company', '0005_auto_20190525_2356'), ('company', '0006_supplierpricebreak_currency'), ('company', '0007_remove_supplierpart_lead_time'), ('company', '0008_auto_20190913_1407'), ('company', '0009_auto_20191118_2323'), ('company', '0010_auto_20200201_1231'), ('company', '0011_auto_20200318_1114'), ('company', '0012_auto_20200318_1114'), ('company', '0013_auto_20200406_0131'), ('company', '0014_auto_20200407_0116'), ('company', '0015_company_is_manufacturer'), ('company', '0016_auto_20200412_2330'), ('company', '0017_auto_20200413_0320'), ('company', '0018_supplierpart_manufacturer'), ('company', '0019_auto_20200413_0642'), ('company', '0020_auto_20200413_0839'), ('company', '0021_remove_supplierpart_manufacturer_name')]
    dependencies = [('common', '0003_auto_20190902_2310'), ('company', '0001_initial'), ('part', '0001_initial')]
    operations = [migrations.AddField(model_name='supplierpart', name='part', field=models.ForeignKey(help_text='Select part', limit_choices_to={'purchaseable': True}, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_parts', to='part.part')), migrations.AddField(model_name='supplierpart', name='supplier', field=models.ForeignKey(help_text='Select supplier', limit_choices_to={'is_supplier': True}, on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='company.company')), migrations.AddField(model_name='contact', name='company', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='company.company')), migrations.AlterUniqueTogether(name='supplierpricebreak', unique_together={('part', 'quantity')}), migrations.AlterUniqueTogether(name='supplierpart', unique_together={('part', 'supplier', 'SKU')}), migrations.RemoveField(model_name='supplierpart', name='minimum'), migrations.AlterField(model_name='supplierpart', name='part', field=models.ForeignKey(help_text='Select part', limit_choices_to={'is_template': False, 'purchaseable': True}, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_parts', to='part.part')), migrations.AddField(model_name='supplierpricebreak', name='currency', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.currency')), migrations.RemoveField(model_name='supplierpart', name='lead_time'), migrations.AlterField(model_name='company', name='notes', field=models.TextField(blank=True)), migrations.AlterField(model_name='supplierpricebreak', name='cost', field=InvenTree.fields.RoundingDecimalField(decimal_places=5, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])), migrations.AlterField(model_name='supplierpricebreak', name='quantity', field=InvenTree.fields.RoundingDecimalField(decimal_places=5, default=1, max_digits=15, validators=[django.core.validators.MinValueValidator(1)])), migrations.RenameField(model_name='company', old_name='URL', new_name='link'), migrations.AlterField(model_name='company', name='link', field=InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external company information', max_length=2000)), migrations.RenameField(model_name='supplierpart', old_name='URL', new_name='link'), migrations.AlterField(model_name='supplierpart', name='link', field=InvenTree.fields.InvenTreeURLField(blank=True, help_text='URL for external supplier part link', max_length=2000)), migrations.AlterField(model_name='company', name='image', field=stdimage.models.StdImageField(blank=True, force_min_size=False, null=True, upload_to=company.models.rename_company_image, variations={})), migrations.AddField(model_name='company', name='is_manufacturer', field=models.BooleanField(default=False, help_text='Does this company manufacture parts?')), migrations.RenameField(model_name='supplierpart', old_name='manufacturer', new_name='manufacturer_name'), migrations.AddField(model_name='supplierpart', name='manufacturer', field=models.ForeignKey(blank=True, help_text='Select manufacturer', limit_choices_to={'is_manufacturer': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manufactured_parts', to='company.company')), migrations.RunPython(migrations.RunPython.noop, reverse_code=migrations.RunPython.noop), migrations.AlterField(model_name='supplierpart', name='supplier', field=models.ForeignKey(help_text='Select supplier', limit_choices_to={'is_supplier': True}, on_delete=django.db.models.deletion.CASCADE, related_name='supplied_parts', to='company.company')), migrations.RemoveField(model_name='supplierpart', name='manufacturer_name')]