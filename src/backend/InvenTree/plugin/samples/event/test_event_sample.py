"""Unit tests for event_sample sample plugins."""

from django.conf import settings
from django.test import TestCase

from common.models import InvenTreeSetting
from InvenTree.unit_test import get_plugin_config
from plugin import InvenTreePlugin
from plugin.base.event.events import trigger_event
from plugin.helpers import MixinNotImplementedError
from plugin.mixins import EventMixin

from .event_sample import logger


class EventPluginSampleTests(TestCase):
    """Tests for EventPluginSample."""

    def test_run_event(self):
        """Check if the event is issued."""
        # Activate plugin
        config = get_plugin_config('sampleevent')
        config.active = True
        config.save()

        InvenTreeSetting.set_setting('ENABLE_PLUGINS_EVENTS', True, change_user=None)

        # Enable event testing
        settings.PLUGIN_TESTING_EVENTS = True
        # Check that an event is issued
        with self.assertLogs(logger=logger, level='DEBUG') as cm:
            trigger_event('test.event')
        self.assertIn(
            'DEBUG:inventree:Event `test.event` triggered in sample plugin', cm[1]
        )

        # Disable again
        settings.PLUGIN_TESTING_EVENTS = False

    def test_mixin(self):
        """Test that MixinNotImplementedError is raised."""
        with self.assertRaises(MixinNotImplementedError):

            class Wrong(EventMixin, InvenTreePlugin):
                pass

            plugin = Wrong()
            plugin.process_event('abc')
