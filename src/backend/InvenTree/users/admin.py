"""Admin classes for the 'users' app."""

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import ApiToken, Owner, RuleSet
from users.ruleset import RULESET_CHOICES

User = get_user_model()


@admin.register(ApiToken)
class ApiTokenAdmin(admin.ModelAdmin):
    """Admin class for the ApiToken model."""

    list_display = ('token', 'user', 'name', 'expiry', 'active', 'version')
    list_filter = ('user', 'revoked', 'version')
    actions = ['disable_v1_tokens']

    @admin.action(description=_('Disable all old (v1) tokens'))
    def disable_v1_tokens(self, request, queryset):
        """Disable all v1 tokens."""
        # Note: we ignore the queryset and disable ALL v1 tokens
        v1_tokens = ApiToken.objects.filter(version=1, revoked=False)
        count = v1_tokens.count()
        v1_tokens.update(revoked=True)
        self.message_user(request, _(f'Disabled {count} old tokens.'))

    fields = (
        'token',
        'user',
        'name',
        'version',
        'created',
        'last_seen',
        'revoked',
        'expiry',
        'metadata',
    )

    def get_fields(self, request, obj=None):
        """Return list of fields to display."""
        fields = ['token'] if obj else ['key']

        if obj and obj.version == 1:
            fields.insert(0, 'v1_warning')

        fields += [
            'user',
            'name',
            'version',
            'created',
            'last_seen',
            'revoked',
            'expiry',
            'metadata',
        ]

        return fields

    def get_readonly_fields(self, request, obj=None):
        """Some fields are read-only after creation."""
        ro = ['created', 'last_seen', 'version', 'token_hash', 'pepper_id']

        if obj:
            ro += ['token', 'user', 'expiry', 'name']

            # Add warning for v1 tokens
            if obj.version == 1:
                from django.utils.safestring import mark_safe

                obj.v1_warning = mark_safe(
                    '<div style="color: red; font-weight: bold; padding: 10px; border: 1px solid red;">'
                    + str(
                        _(
                            'This is an old (v1) token. It is stored in plaintext and should be replaced.'
                        )
                    )
                    + '</div>'
                )
                ro.append('v1_warning')

        return ro

    def v1_warning(self, obj):
        """Return warning message for v1 tokens."""
        return getattr(obj, 'v1_warning', '')


class RuleSetInline(admin.TabularInline):
    """Class for displaying inline RuleSet data in the Group admin page."""

    model = RuleSet
    can_delete = False
    verbose_name = 'Ruleset'
    verbose_plural_name = 'Rulesets'
    fields = ['name', *list(RuleSet.RULE_OPTIONS)]
    readonly_fields = ['name']
    max_num = len(RULESET_CHOICES)
    min_num = 1
    extra = 0
    ordering = ['name']


class InvenTreeGroupAdminForm(forms.ModelForm):
    """Custom admin form for the Group model.

    Adds the ability for editing user membership directly in the group admin page.
    """

    class Meta:
        """Metaclass defines extra fields."""

        model = Group
        exclude = []
        fields = ['name', 'users']

    def __init__(self, *args, **kwargs):  # pragma: no cover
        """Populate the 'users' field with the users in the current group."""
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('users', False),
        label=_('Users'),
        help_text=_('Select which users are assigned to this group'),
    )

    def save_m2m(self):  # pragma: no cover
        """Add the users to the Group."""
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):  # pragma: no cover
        """Custom save method for Group admin form."""
        # Default save
        instance = super().save()
        # Save many-to-many data
        self.save_m2m()
        return instance


class InvenTreeUserAdmin(UserAdmin):
    """Custom admin page for the User model.

    - Restrict user creation and editing to superuser accounts
    - Hides the "permissions" view as this is handled by RuleSets
    """

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'last_login',
    )  # display last connection for each user in user admin panel.

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')},
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make all fields read-only for non-superusers."""
        fields = super().get_readonly_fields(request, obj)

        if not request.user.is_superuser:
            fields += ('is_staff', 'is_superuser')

        return fields


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    """Custom admin interface for the Owner model."""

    search_fields = ['name']


admin.site.unregister(User)
admin.site.register(User, InvenTreeUserAdmin)
