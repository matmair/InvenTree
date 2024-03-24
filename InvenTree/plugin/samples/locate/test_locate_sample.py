"""Unit tests for locate_sample sample plugins."""

from django.urls import reverse

from InvenTree.unit_test import InvenTreeAPITestCase, get_plugin_config
from plugin import InvenTreePlugin, registry
from plugin.helpers import MixinNotImplementedError
from plugin.mixins import LocateMixin


class SampleLocatePlugintests(InvenTreeAPITestCase):
    """Tests for SampleLocatePlugin."""

    fixtures = ['location', 'category', 'part', 'stock']

    def test_run_locator(self):
        """Check if the event is issued."""
        # Activate plugin
        config = get_plugin_config('samplelocate')
        config.active = True
        config.save()

        # Test APIs
        url = reverse('api-locate-plugin')

        # No plugin
        self.post(url, {}, expected_code=400)

        # Wrong plugin
        self.post(url, {'plugin': 'sampleevent'}, expected_code=400)

        # Right plugin - no search item
        self.post(url, {'plugin': 'samplelocate'}, expected_code=400)

        # Right plugin - wrong reference
        self.post(url, {'plugin': 'samplelocate', 'item': 999}, expected_code=404)

        # Right plugin - right reference
        self.post(url, {'plugin': 'samplelocate', 'item': 1}, expected_code=200)

        # Right plugin - wrong reference
        self.post(url, {'plugin': 'samplelocate', 'location': 999}, expected_code=404)

        # Right plugin - right reference
        self.post(url, {'plugin': 'samplelocate', 'location': 1}, expected_code=200)

    def test_mixin(self):
        """Test that MixinNotImplementedError is raised."""
        # Test location locator
        with self.assertRaises(MixinNotImplementedError):

            class Wrong(LocateMixin, InvenTreePlugin):
                pass

            plugin = Wrong()
            plugin.locate_stock_location(1)

        # Test item locator
        with self.assertRaises(MixinNotImplementedError):
            plugin.locate_stock_item(1)
