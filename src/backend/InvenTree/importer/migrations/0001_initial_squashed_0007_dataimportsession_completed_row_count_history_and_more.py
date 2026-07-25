import django.core.validators
import django.db.models.deletion
import importer.validators
from django.conf import settings
from django.db import migrations, models
import importlib

def get_migration_func(migration_name, func_name):
    try:
        mod = importlib.import_module(f'importer.migrations.{migration_name}')
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
    replaces = [('importer', '0001_initial'), ('importer', '0002_dataimportsession_field_overrides'), ('importer', '0003_dataimportsession_field_filters'), ('importer', '0004_alter_dataimportsession_model_type'), ('importer', '0005_dataimportsession_update_records'), ('importer', '0006_dataimportcolumnmap_lookup_field'), ('importer', '0007_dataimportsession_completed_row_count_history_and_more')]
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name='DataImportSession', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')), ('data_file', models.FileField(help_text='Data file to import', upload_to='import', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv', 'xlsx', 'tsv']), importer.validators.validate_data_file], verbose_name='Data File')), ('columns', models.JSONField(blank=True, null=True, verbose_name='Columns')), ('model_type', models.CharField(help_text='Target model type for this import session', max_length=100, validators=[importer.validators.validate_importer_model_type], verbose_name='Model Type')), ('status', models.PositiveIntegerField(choices=[(0, 'Initializing'), (10, 'Mapping Columns'), (20, 'Importing Data'), (30, 'Processing Data'), (40, 'Complete')], default=0, help_text='Import status')), ('field_defaults', models.JSONField(blank=True, null=True, validators=[importer.validators.validate_field_defaults], verbose_name='Field Defaults')), ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')), ('field_overrides', models.JSONField(blank=True, null=True, validators=[importer.validators.validate_field_defaults], verbose_name='Field Overrides')), ('field_filters', models.JSONField(blank=True, null=True, validators=[importer.validators.validate_field_defaults], verbose_name='Field Filters')), ('update_records', models.BooleanField(default=False, help_text='If enabled, existing records will be updated with new data', verbose_name='Update Existing Records')), ('completed_row_count_history', models.PositiveIntegerField(blank=True, null=True, verbose_name='Completed Row Count History')), ('row_count_history', models.PositiveIntegerField(blank=True, null=True, verbose_name='Row Count History'))]), migrations.CreateModel(name='DataImportRow', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('row_index', models.PositiveIntegerField(default=0, verbose_name='Row Index')), ('row_data', models.JSONField(blank=True, null=True, verbose_name='Original row data')), ('data', models.JSONField(blank=True, null=True, verbose_name='Data')), ('errors', models.JSONField(blank=True, null=True, verbose_name='Errors')), ('valid', models.BooleanField(default=False, verbose_name='Valid')), ('complete', models.BooleanField(default=False, verbose_name='Complete')), ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='importer.dataimportsession', verbose_name='Import Session'))]), migrations.CreateModel(name='DataImportColumnMap', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('field', models.CharField(max_length=100, verbose_name='Field')), ('column', models.CharField(blank=True, max_length=100, verbose_name='Column')), ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='column_mappings', to='importer.dataimportsession', verbose_name='Import Session')), ('lookup_field', models.CharField(blank=True, help_text='Database field to use for foreign-key lookup. Leave blank for automatic lookup.', max_length=100, null=True, verbose_name='Lookup Field'))])]