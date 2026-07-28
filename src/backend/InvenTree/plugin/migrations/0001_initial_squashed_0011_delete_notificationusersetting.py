import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import importlib

def get_migration_func(migration_name, func_name):
    try:
        mod = importlib.import_module(f'plugin.migrations.{migration_name}')
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
    replaces = [('plugin', '0001_initial'), ('plugin', '0002_alter_pluginconfig_options'), ('plugin', '0003_pluginsetting'), ('plugin', '0004_alter_pluginsetting_key'), ('plugin', '0005_notificationusersetting'), ('plugin', '0006_pluginconfig_metadata'), ('plugin', '0007_auto_20230805_1748'), ('plugin', '0008_pluginconfig_package_name'), ('plugin', '0009_alter_pluginconfig_key'), ('plugin', '0010_pluginusersetting'), ('plugin', '0011_delete_notificationusersetting')]
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name='PluginConfig', fields=[('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('key', models.CharField(db_index=True, help_text='Key of plugin', max_length=255, unique=True, verbose_name='Key')), ('name', models.CharField(blank=True, help_text='Name of the plugin', max_length=255, null=True, verbose_name='Name')), ('active', models.BooleanField(default=False, help_text='Is the plugin active', verbose_name='Active')), ('metadata', models.JSONField(blank=True, help_text='JSON metadata field, for use by external plugins', null=True, verbose_name='Plugin Metadata')), ('package_name', models.CharField(blank=True, help_text='Name of the installed package, if the plugin was installed via PIP', max_length=255, null=True, verbose_name='Package Name'))], options={'verbose_name': 'Plugin Configuration', 'verbose_name_plural': 'Plugin Configurations'}), migrations.CreateModel(name='PluginSetting', fields=[('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('key', models.CharField(help_text='Settings key', max_length=50)), ('value', models.CharField(blank=True, help_text='Settings value', max_length=2000)), ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='plugin.pluginconfig', verbose_name='Plugin'))], options={'unique_together': {('plugin', 'key')}}), migrations.CreateModel(name='PluginUserSetting', fields=[('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('key', models.CharField(help_text='Settings key', max_length=50)), ('value', models.CharField(blank=True, help_text='Settings value', max_length=2000)), ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_settings', to='plugin.pluginconfig', verbose_name='Plugin')), ('user', models.ForeignKey(help_text='User', on_delete=django.db.models.deletion.CASCADE, related_name='plugin_settings', to=settings.AUTH_USER_MODEL, verbose_name='User'))], options={'unique_together': {('plugin', 'user', 'key')}})]