"""Build status codes."""

from django.utils.translation import gettext_lazy as _

from generic.states import StatusCode


class BuildStatus(StatusCode):
    """Build status codes."""

    PENDING = 10, _('Pending'), 'secondary'  # Build is pending / active
    PRODUCTION = 20, _('Production'), 'primary'  # Build is in production
    ON_HOLD = 25, _('On Hold'), 'warning'  # Build is on hold
    CANCELLED = 30, _('Cancelled'), 'danger'  # Build was cancelled
    COMPLETE = 40, _('Complete'), 'success'  # Build is complete


class BuildStatusGroups:
    """Groups for BuildStatus codes."""

    ACTIVE_CODES = [
        BuildStatus.PENDING.value,
        BuildStatus.ON_HOLD.value,
        BuildStatus.PRODUCTION.value,
    ]
