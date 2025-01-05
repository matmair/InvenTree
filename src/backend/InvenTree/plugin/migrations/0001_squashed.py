# Generated by Django 4.2.17 on 2025-01-05 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    replaces = [
        ("plugin", "0001_initial"),
        ("plugin", "0002_alter_pluginconfig_options"),
        ("plugin", "0003_pluginsetting"),
        ("plugin", "0004_alter_pluginsetting_key"),
        ("plugin", "0005_notificationusersetting"),
        ("plugin", "0006_pluginconfig_metadata"),
        ("plugin", "0007_auto_20230805_1748"),
        ("plugin", "0008_pluginconfig_package_name"),
        ("plugin", "0009_alter_pluginconfig_key"),
    ]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PluginConfig",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        blank=True,
                        help_text="JSON metadata field, for use by external plugins",
                        null=True,
                        verbose_name="Plugin Metadata",
                    ),
                ),
                (
                    "key",
                    models.CharField(
                        db_index=True,
                        help_text="Key of plugin",
                        max_length=255,
                        unique=True,
                        verbose_name="Key",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="PluginName of the plugin",
                        max_length=255,
                        null=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "package_name",
                    models.CharField(
                        blank=True,
                        help_text="Name of the installed package, if the plugin was installed via PIP",
                        max_length=255,
                        null=True,
                        verbose_name="Package Name",
                    ),
                ),
                (
                    "active",
                    models.BooleanField(
                        default=False,
                        help_text="Is the plugin active",
                        verbose_name="Active",
                    ),
                ),
            ],
            options={
                "verbose_name": "Plugin Configuration",
                "verbose_name_plural": "Plugin Configurations",
            },
        ),
        migrations.CreateModel(
            name="PluginSetting",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key", models.CharField(help_text="Settings key", max_length=50)),
                (
                    "value",
                    models.CharField(
                        blank=True, help_text="Settings value", max_length=2000
                    ),
                ),
                (
                    "plugin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="settings",
                        to="plugin.pluginconfig",
                        verbose_name="Plugin",
                    ),
                ),
            ],
            options={
                "unique_together": {("plugin", "key")},
            },
        ),
        migrations.CreateModel(
            name="NotificationUserSetting",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key", models.CharField(help_text="Settings key", max_length=50)),
                (
                    "value",
                    models.CharField(
                        blank=True, help_text="Settings value", max_length=2000
                    ),
                ),
                ("method", models.CharField(max_length=255, verbose_name="Method")),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        help_text="User",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "unique_together": {("method", "user", "key")},
            },
        ),
    ]
