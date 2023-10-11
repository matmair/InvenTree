"""AppConfig for inventree app."""

import logging
from importlib import import_module
from pathlib import Path

from django.apps import AppConfig, apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import AppRegistryNotReady
from django.db import transaction
from django.db.utils import IntegrityError, OperationalError

import InvenTree.conversion
import InvenTree.tasks
from InvenTree.config import get_setting
from InvenTree.ready import (canAppAccessDatabase, isInMainThread,
                             isInTestMode, isPluginRegistryLoaded)

logger = logging.getLogger("inventree")


class InvenTreeConfig(AppConfig):
    """AppConfig for inventree app."""
    name = 'InvenTree'

    def ready(self):
        """Run system wide setup init steps.

        Like:
        - Checking if migrations should be run
        - Cleaning up tasks
        - Starting regular tasks
        - Updating exchange rates
        - Collecting notification methods
        - Adding users set in the current environment
        """
        # skip loading if plugin registry is not loaded or we run in a background thread
        if not isPluginRegistryLoaded() or not isInMainThread():
            return

        if canAppAccessDatabase() or settings.TESTING_ENV:

            self.remove_obsolete_tasks()

            self.collect_tasks()
            self.start_background_tasks()

            if not isInTestMode():  # pragma: no cover
                self.update_exchange_rates()
                # Let the background worker check for migrations
                InvenTree.tasks.offload_task(InvenTree.tasks.check_for_migrations)

        self.collect_notification_methods()

        # Ensure the unit registry is loaded
        InvenTree.conversion.get_unit_registry()

        if canAppAccessDatabase() or settings.TESTING_ENV:
            self.add_user_on_startup()

    def remove_obsolete_tasks(self):
        """Delete any obsolete scheduled tasks in the database."""
        obsolete = [
            'InvenTree.tasks.delete_expired_sessions',
            'stock.tasks.delete_old_stock_items',
        ]

        try:
            from django_q.models import Schedule
        except AppRegistryNotReady:  # pragma: no cover
            return

        # Remove any existing obsolete tasks
        try:
            Schedule.objects.filter(func__in=obsolete).delete()
        except Exception:
            logger.exception("Failed to remove obsolete tasks - database not ready")

    def start_background_tasks(self):
        """Start all background tests for InvenTree."""

        logger.info("Starting background tasks...")

        # List of collected tasks found with the @scheduled_task decorator
        tasks = InvenTree.tasks.tasks.task_list

        for task in tasks:
            ref_name = f'{task.func.__module__}.{task.func.__name__}'
            InvenTree.tasks.schedule_task(
                ref_name,
                schedule_type=task.interval,
                minutes=task.minutes,
            )

        # Put at least one task onto the background worker stack,
        # which will be processed as soon as the worker comes online
        InvenTree.tasks.offload_task(
            InvenTree.tasks.heartbeat,
            force_async=True,
        )

        logger.info("Started %s scheduled background tasks...", len(tasks))

    def collect_tasks(self):
        """Collect all background tasks."""

        for app_name, app in apps.app_configs.items():
            if app_name == 'InvenTree':
                continue

            if Path(app.path).joinpath('tasks.py').exists():
                try:
                    import_module(f'{app.module.__package__}.tasks')
                except Exception as e:  # pragma: no cover
                    logger.exception("Error loading tasks for %s: %s", app_name, e)

    def update_exchange_rates(self):  # pragma: no cover
        """Update exchange rates each time the server is started.

        Only runs *if*:
        a) Have not been updated recently (one day or less)
        b) The base exchange rate has been altered
        """
        try:
            from djmoney.contrib.exchange.models import ExchangeBackend

            from common.settings import currency_code_default
            from InvenTree.tasks import update_exchange_rates
        except AppRegistryNotReady:  # pragma: no cover
            pass

        base_currency = currency_code_default()

        update = False

        try:
            backend = ExchangeBackend.objects.filter(name='InvenTreeExchange')

            if backend.exists():
                backend = backend.first()

                last_update = backend.last_update

                if last_update is None:
                    # Never been updated
                    logger.info("Exchange backend has never been updated")
                    update = True

                # Backend currency has changed?
                if base_currency != backend.base_currency:
                    logger.info("Base currency changed from %s to %s", backend.base_currency, base_currency)
                    update = True

        except (ExchangeBackend.DoesNotExist):
            logger.info("Exchange backend not found - updating")
            update = True

        except Exception:
            # Some other error - potentially the tables are not ready yet
            return

        if update:
            try:
                update_exchange_rates()
            except OperationalError:
                logger.warning("Could not update exchange rates - database not ready")
            except Exception as e:
                logger.exception("Error updating exchange rates: %s (%s)", e, type(e))

    def add_user_on_startup(self):
        """Add a user on startup."""
        # stop if checks were already created
        if hasattr(settings, 'USER_ADDED') and settings.USER_ADDED:
            return

        # get values
        add_user = get_setting('INVENTREE_ADMIN_USER', 'admin_user')
        add_email = get_setting('INVENTREE_ADMIN_EMAIL', 'admin_email')
        add_password = get_setting('INVENTREE_ADMIN_PASSWORD', 'admin_password')

        # check if all values are present
        set_variables = 0

        for tested_var in [add_user, add_email, add_password]:
            if tested_var:
                set_variables += 1

        # no variable set -> do not try anything
        if set_variables == 0:
            settings.USER_ADDED = True
            return

        # not all needed variables set
        if set_variables < 3:
            logger.warning('Not all required settings for adding a user on startup are present:\nINVENTREE_ADMIN_USER, INVENTREE_ADMIN_EMAIL, INVENTREE_ADMIN_PASSWORD')
            settings.USER_ADDED = True
            return

        # good to go -> create user
        user = get_user_model()
        try:
            with transaction.atomic():
                if user.objects.filter(username=add_user).exists():
                    logger.info("User %s already exists - skipping creation", add_user)
                else:
                    new_user = user.objects.create_superuser(add_user, add_email, add_password)
                    logger.info('User %s was created!', str(new_user))
        except IntegrityError:
            logger.warning('The user "%s" could not be created', add_user)

        # do not try again
        settings.USER_ADDED = True

    def collect_notification_methods(self):
        """Collect all notification methods."""
        from common.notifications import storage

        storage.collect()
