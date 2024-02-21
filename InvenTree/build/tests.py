"""Basic unit tests for the BuildOrder app"""

from datetime import datetime, timedelta

from InvenTree.unit_test import InvenTreeTestCase

from .models import Build

from InvenTree.status_codes import BuildStatus


class BuildTestSimple(InvenTreeTestCase):
    """Basic set of tests for the BuildOrder model functionality"""

    fixtures = [
        'category',
        'part',
        'location',
        'build',
    ]

    roles = [
        'build.change',
        'build.add',
        'build.delete',
    ]

    def test_build_objects(self):
        """Ensure the Build objects were correctly created"""
        self.assertEqual(Build.objects.count(), 5)
        b = Build.objects.get(pk=2)
        self.assertEqual(b.batch, 'B2')
        self.assertEqual(b.quantity, 21)

        self.assertEqual(str(b), 'BO-0002')

    def test_url(self):
        """Test URL lookup"""
        b1 = Build.objects.get(pk=1)
        self.assertEqual(b1.get_absolute_url(), 'TOBEREFACTORED')

    def test_is_complete(self):
        """Test build completion status"""
        b1 = Build.objects.get(pk=1)
        b2 = Build.objects.get(pk=2)

        self.assertEqual(b1.is_complete, False)
        self.assertEqual(b2.is_complete, True)

        self.assertEqual(b2.status, BuildStatus.COMPLETE)

    def test_overdue(self):
        """Test overdue status functionality."""
        today = datetime.now().date()

        build = Build.objects.get(pk=1)
        self.assertFalse(build.is_overdue)

        build.target_date = today - timedelta(days=1)
        build.save()
        self.assertTrue(build.is_overdue)

        build.target_date = today + timedelta(days=80)
        build.save()
        self.assertFalse(build.is_overdue)

    def test_is_active(self):
        """Test active / inactive build status"""
        b1 = Build.objects.get(pk=1)
        b2 = Build.objects.get(pk=2)

        self.assertEqual(b1.is_active, True)
        self.assertEqual(b2.is_active, False)

    def test_cancel_build(self):
        """Test build cancellation function."""
        build = Build.objects.get(id=1)

        self.assertEqual(build.status, BuildStatus.PENDING)

        build.cancel_build(self.user)

        self.assertEqual(build.status, BuildStatus.CANCELLED)
