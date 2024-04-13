"""Admin for the common app."""

from django.contrib import admin

import common.models


class SettingsAdmin(admin.ModelAdmin):
    """Admin settings for InvenTreeSetting."""

    list_display = ('key', 'value')

    def get_readonly_fields(self, request, obj=None):  # pragma: no cover
        """Prevent the 'key' field being edited once the setting is created."""
        if obj:
            return ['key']
        return []


class UserSettingsAdmin(admin.ModelAdmin):
    """Admin settings for InvenTreeUserSetting."""

    list_display = ('key', 'value', 'user')

    def get_readonly_fields(self, request, obj=None):  # pragma: no cover
        """Prevent the 'key' field being edited once the setting is created."""
        if obj:
            return ['key']
        return []


class WebhookAdmin(admin.ModelAdmin):
    """Admin settings for Webhook."""

    list_display = ('endpoint_id', 'name', 'active', 'user')


class NotificationEntryAdmin(admin.ModelAdmin):
    """Admin settings for NotificationEntry."""

    list_display = ('key', 'uid', 'updated')


class NotificationMessageAdmin(admin.ModelAdmin):
    """Admin settings for NotificationMessage."""

    list_display = (
        'age_human',
        'user',
        'category',
        'name',
        'read',
        'target_object',
        'source_object',
    )

    list_filter = ('category', 'read', 'user')

    search_fields = ('name', 'category', 'message')


class NewsFeedEntryAdmin(admin.ModelAdmin):
    """Admin settings for NewsFeedEntry."""

    list_display = ('title', 'author', 'published', 'summary')


admin.site.register(common.models.InvenTreeSetting, SettingsAdmin)
admin.site.register(common.models.InvenTreeUserSetting, UserSettingsAdmin)
admin.site.register(common.models.WebhookEndpoint, WebhookAdmin)
admin.site.register(common.models.WebhookMessage, admin.ModelAdmin)
admin.site.register(common.models.NotificationEntry, NotificationEntryAdmin)
admin.site.register(common.models.NotificationMessage, NotificationMessageAdmin)
admin.site.register(common.models.NewsFeedEntry, NewsFeedEntryAdmin)
