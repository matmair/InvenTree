"""Unit tests for event_sample sample plugins."""

from django.test import TestCase

from common.models import InvenTreeSetting
from plugin import registry
from plugin.base.event.events import trigger_event


class FilteredEventPluginSampleTests(TestCase):
    """Tests for EventPluginSample."""

    def test_run_event(self):
        """Check if the event is issued."""
        # Activate plugin
        registry.set_plugin_state('filteredsampleevent', True)

        InvenTreeSetting.set_setting('ENABLE_PLUGINS_EVENTS', True, change_user=None)

        # Enable event testing
        with self.settings(PLUGIN_TESTING_EVENTS=True):
            # Check that an event is issued
            with self.assertLogs(logger='inventree', level='DEBUG') as cm:
                trigger_event('test.event')
            self.assertIn('Event `test.event` triggered in sample plugin', str(cm[1]))

    def test_ignore_event(self):
        """Check if the event is issued."""
        # Activate plugin
        registry.set_plugin_state('filteredsampleevent', True)

        InvenTreeSetting.set_setting('ENABLE_PLUGINS_EVENTS', True, change_user=None)

        # Enable event testing
        with self.settings(PLUGIN_TESTING_EVENTS=True):
            # Check that an event is issued
            with self.assertLogs(logger='inventree', level='DEBUG') as cm:
                trigger_event('test.some.other.event')
            self.assertNotIn(
                'DEBUG:inventree:Event `test.some.other.event` triggered in sample plugin',
                cm[1],
            )
