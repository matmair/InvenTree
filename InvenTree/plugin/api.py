"""
JSON API for the plugin app
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import include, re_path

from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from common.api import GlobalSettingsPermissions
from plugin.models import PluginConfig, PluginSetting
import plugin.serializers as PluginSerializers
from plugin.registry import registry


class PluginList(generics.ListAPIView):
    """ API endpoint for list of PluginConfig objects

    - GET: Return a list of all PluginConfig objects
    """

    # Allow any logged in user to read this endpoint
    # This is necessary to allow certain functionality,
    # e.g. determining which label printing plugins are available
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = PluginSerializers.PluginConfigSerializer
    queryset = PluginConfig.objects.all()

    ordering_fields = [
        'key',
        'name',
        'active',
    ]

    ordering = [
        'key',
    ]

    search_fields = [
        'key',
        'name',
    ]


class PluginDetail(generics.RetrieveUpdateDestroyAPIView):
    """ API detail endpoint for PluginConfig object

    get:
    Return a single PluginConfig object

    post:
    Update a PluginConfig

    delete:
    Remove a PluginConfig
    """

    queryset = PluginConfig.objects.all()
    serializer_class = PluginSerializers.PluginConfigSerializer


class PluginInstall(generics.CreateAPIView):
    """
    Endpoint for installing a new plugin
    """
    queryset = PluginConfig.objects.none()
    serializer_class = PluginSerializers.PluginConfigInstallSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.perform_create(serializer)
        result['input'] = serializer.data
        headers = self.get_success_headers(serializer.data)
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class PluginSettingList(generics.ListAPIView):
    """
    List endpoint for all plugin related settings.

    - read only
    - only accessible by staff users
    """

    queryset = PluginSetting.objects.all()
    serializer_class = PluginSerializers.PluginSettingSerializer

    permission_classes = [
        GlobalSettingsPermissions,
    ]

    filter_backends = [
        DjangoFilterBackend,
    ]

    filter_fields = [
        'plugin__active',
        'plugin__key',
    ]


class PluginSettingDetail(generics.RetrieveUpdateAPIView):
    """
    Detail endpoint for a plugin-specific setting.

    Note that these cannot be created or deleted via the API
    """

    queryset = PluginSetting.objects.all()
    serializer_class = PluginSerializers.PluginSettingSerializer

    def get_object(self):
        """
        Lookup the plugin setting object, based on the URL.
        The URL provides the 'slug' of the plugin, and the 'key' of the setting.

        Both the 'slug' and 'key' must be valid, else a 404 error is raised
        """

        plugin_slug = self.kwargs['plugin']
        key = self.kwargs['key']

        # Check that the 'plugin' specified is valid!
        if not PluginConfig.objects.filter(key=plugin_slug).exists():
            raise NotFound(detail=f"Plugin '{plugin_slug}' not installed")

        # Get the list of settings available for the specified plugin
        plugin = registry.get_plugin(plugin_slug)

        if plugin is None:
            raise NotFound(detail=f"Plugin '{plugin_slug}' not found")

        settings = getattr(plugin, 'SETTINGS', {})

        if key not in settings:
            raise NotFound(detail=f"Plugin '{plugin_slug}' has no setting matching '{key}'")

        return PluginSetting.get_setting_object(key, plugin=plugin)

    # Staff permission required
    permission_classes = [
        GlobalSettingsPermissions,
    ]


plugin_api_urls = [

    # Plugin settings URLs
    re_path(r'^settings/', include([
        re_path(r'^(?P<plugin>\w+)/(?P<key>\w+)/', PluginSettingDetail.as_view(), name='api-plugin-setting-detail'),
        re_path(r'^.*$', PluginSettingList.as_view(), name='api-plugin-setting-list'),
    ])),

    # Detail views for a single PluginConfig item
    re_path(r'^(?P<pk>\d+)/', include([
        re_path(r'^.*$', PluginDetail.as_view(), name='api-plugin-detail'),
    ])),

    re_path(r'^install/', PluginInstall.as_view(), name='api-plugin-install'),

    # Anything else
    re_path(r'^.*$', PluginList.as_view(), name='api-plugin-list'),
]
