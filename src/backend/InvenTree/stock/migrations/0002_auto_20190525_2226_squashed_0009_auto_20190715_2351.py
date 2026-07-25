import InvenTree.validators
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models
import importlib

def get_migration_func(migration_name, func_name):
    try:
        mod = importlib.import_module(f'stock.migrations.{migration_name}')
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
    replaces = [('stock', '0002_auto_20190525_2226'), ('stock', '0003_auto_20190525_2303'), ('stock', '0004_auto_20190525_2356'), ('stock', '0005_auto_20190602_1944'), ('stock', '0006_stockitem_purchase_order'), ('stock', '0007_auto_20190618_0042'), ('stock', '0008_stockitemtracking_url'), ('stock', '0009_auto_20190715_2351')]
    dependencies = [('order', '0010_purchaseorderlineitem_notes'), ('stock', '0001_initial')]
    operations = [migrations.AlterField(model_name='stockitem', name='part', field=models.ForeignKey(help_text='Base part', limit_choices_to={'active': True, 'is_template': False}, on_delete=django.db.models.deletion.CASCADE, related_name='stock_items', to='part.part')), migrations.AlterField(model_name='stockitem', name='status', field=models.PositiveIntegerField(choices=[(10, 'OK'), (50, 'Attention needed'), (55, 'Damaged'), (60, 'Destroyed'), (70, 'Lost')], default=10, validators=[django.core.validators.MinValueValidator(0)])), migrations.AddField(model_name='stockitem', name='purchase_order', field=models.ForeignKey(blank=True, help_text='Purchase order for this stock item', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_items', to='order.purchaseorder')), migrations.AlterField(model_name='stocklocation', name='name', field=models.CharField(max_length=100, unique=True, validators=[InvenTree.validators.validate_tree_name])), migrations.AddField(model_name='stockitemtracking', name='URL', field=models.URLField(blank=True, help_text='Link to external page for further information')), migrations.AlterField(model_name='stockitemtracking', name='notes', field=models.CharField(blank=True, help_text='Entry notes', max_length=512)), migrations.AlterField(model_name='stockitemtracking', name='title', field=models.CharField(help_text='Tracking entry title', max_length=250))]