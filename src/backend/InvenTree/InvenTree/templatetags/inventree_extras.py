"""This module provides template tags for extra functionality, over and above the built-in Django tags."""

import logging
from datetime import date, datetime

from django import template
from django.conf import settings as djangosettings

import common.models
import InvenTree.helpers
import InvenTree.helpers_model
from common.settings import get_global_setting
from InvenTree import version
from plugin import registry

register = template.Library()


logger = logging.getLogger('inventree')


@register.simple_tag()
def define(value, *args, **kwargs):
    """Shortcut function to overcome the shortcomings of the django templating language.

    Use as follows: {% define "hello_world" as hello %}

    Ref: https://stackoverflow.com/questions/1070398/how-to-set-a-value-of-a-variable-inside-a-template-code
    """
    return value


@register.simple_tag()
def decimal(x, *args, **kwargs):
    """Simplified rendering of a decimal number."""
    return InvenTree.helpers.decimal2string(x)


@register.simple_tag(takes_context=True)
def render_date(context, date_object):
    """Renders a date according to the preference of the provided user.

    Note that the user preference is stored using the formatting adopted by moment.js,
    which differs from the python formatting!
    """
    if date_object is None:
        return None

    if isinstance(date_object, str):
        date_object = date_object.strip()

        # Check for empty string
        if len(date_object) == 0:
            return None

        # If a string is passed, first convert it to a datetime
        try:
            date_object = date.fromisoformat(date_object)
        except ValueError:
            logger.warning('Tried to convert invalid date string: %s', date_object)
            return None

    # We may have already pre-cached the date format by calling this already!
    user_date_format = context.get('user_date_format', None)

    if user_date_format is None:
        user = context.get('user', None)

        if user and user.is_authenticated:
            # User is specified - look for their date display preference
            user_date_format = common.models.InvenTreeUserSetting.get_setting(
                'DATE_DISPLAY_FORMAT', user=user
            )
        else:
            user_date_format = 'YYYY-MM-DD'

        # Convert the format string to Pythonic equivalent
        replacements = [('YYYY', '%Y'), ('MMM', '%b'), ('MM', '%m'), ('DD', '%d')]

        for o, n in replacements:
            user_date_format = user_date_format.replace(o, n)

        # Update the context cache
        context['user_date_format'] = user_date_format

    if isinstance(date_object, (datetime, date)):
        return date_object.strftime(user_date_format)
    return date_object


@register.simple_tag
def render_currency(money, **kwargs):
    """Render a currency / Money object."""
    return InvenTree.helpers_model.render_currency(money, **kwargs)


@register.simple_tag()
def str2bool(x, *args, **kwargs):
    """Convert a string to a boolean value."""
    return InvenTree.helpers.str2bool(x)


@register.simple_tag()
def add(x, y, *args, **kwargs):
    """Add two numbers together."""
    return x + y


@register.simple_tag()
def to_list(*args):
    """Return the input arguments as list."""
    return args


@register.simple_tag()
def inventree_show_about(user, *args, **kwargs):
    """Return True if the about modal should be shown."""
    if get_global_setting('INVENTREE_RESTRICT_ABOUT'):
        # Return False if the user is not a superuser, or no user information is provided
        if not user or not user.is_superuser:
            return False

    return True


@register.simple_tag()
def plugins_enabled(*args, **kwargs):
    """Return True if plugins are enabled for the server instance."""
    return djangosettings.PLUGINS_ENABLED


def plugins_info(*args, **kwargs):
    """Return information about activated plugins."""
    # Check if plugins are even enabled
    if not djangosettings.PLUGINS_ENABLED:
        return False

    # Fetch plugins
    plug_list = [plg for plg in registry.plugins.values() if plg.plugin_config().active]
    # Format list
    return [
        {'name': plg.name, 'slug': plg.slug, 'version': plg.version}
        for plg in plug_list
    ]


@register.simple_tag()
def inventree_instance_name(*args, **kwargs):
    """Return the InstanceName associated with the current database."""
    return version.inventreeInstanceName()


@register.simple_tag()
def inventree_title(*args, **kwargs):
    """Return the title for the current instance - respecting the settings."""
    return version.inventreeInstanceTitle()


@register.simple_tag()
def inventree_logo(**kwargs):
    """Return the InvenTree logo, *or* a custom logo if the user has provided one.

    Returns a path to an image file, which can be rendered in the web interface
    """
    return InvenTree.helpers.getLogoImage(**kwargs)


@register.simple_tag()
def inventree_splash(**kwargs):
    """Return the URL for the InvenTree splash screen, *or* a custom screen if the user has provided one."""
    return InvenTree.helpers.getSplashScreen(**kwargs)


@register.simple_tag()
def inventree_version(shortstring=False, *args, **kwargs):
    """Return InvenTree version string."""
    if shortstring:
        return f'{version.inventreeInstanceTitle()} v{version.inventreeVersion()}'
    return version.inventreeVersion()


@register.simple_tag()
def settings_value(key, *args, **kwargs):
    """Return a settings value specified by the given key."""
    if 'user' in kwargs:
        if not kwargs['user'] or (
            kwargs['user'] and kwargs['user'].is_authenticated is False
        ):
            return common.models.InvenTreeUserSetting.get_setting(key)
        return common.models.InvenTreeUserSetting.get_setting(key, user=kwargs['user'])

    return get_global_setting(key)
