"""Custom user model for InvenTree."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class InvenTreeAbstractUserMixin(models.Model):
    """Abstract model mixin for the InvenTreeUser model."""

    class Meta:
        """Metaclass defines model properties."""

        abstract = True

    @staticmethod
    def get_api_url():  # pragma: no cover
        """Return the API endpoint URL for the InvenTreeUser model."""
        return reverse('api-user-list')

    language = models.CharField(
        max_length=10,
        blank=True,
        default='',
        verbose_name=_('Language'),
        help_text=_('User language preference'),
    )
    light_mode = models.BooleanField(
        default=False, verbose_name=_('Light Mode'), help_text=_('Use light mode theme')
    )
    public_language = models.BooleanField(
        default=False,
        verbose_name=_('Public Language'),
        help_text=_('Use public language'),
    )
    avatar_url = models.URLField(
        blank=True,
        default='',
        verbose_name=_('Avatar URL'),
        help_text=_('URL to user avatar image'),
    )

    def __str__(self):
        """Function to override the default Django User __str__."""
        from common.settings import get_global_setting

        if get_global_setting('DISPLAY_FULL_NAMES', cache=True):
            if self.first_name or self.last_name:
                return f'{self.first_name} {self.last_name}'
        return self.username


class InvenTreeUser(InvenTreeAbstractUserMixin, AbstractUser):
    """Custom user model for InvenTree.

    Extends the default Django user model with additional fields.
    """

    class Meta:
        """Metaclass defines model properties."""

        # db_table = 'auth_user'
