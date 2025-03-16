"""Permission set for InvenTree."""

from functools import wraps
from typing import Optional

from oauth2_provider.contrib.rest_framework import TokenMatchesOASRequirements
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from rest_framework import permissions

import users.models


def get_model_for_view(view):
    """Attempt to introspect the 'model' type for an API view."""
    if hasattr(view, 'get_permission_model'):
        return view.get_permission_model()

    if hasattr(view, 'serializer_class'):
        return view.serializer_class.Meta.model

    if hasattr(view, 'get_serializer_class'):
        return view.get_serializer_class().Meta.model

    raise AttributeError(f'Serializer class not specified for {view.__class__}')


class RolePermission(permissions.BasePermission):
    """Role mixin for API endpoints, allowing us to specify the user "role" which is required for certain operations.

    Each endpoint can have one or more of the following actions:
    - GET
    - POST
    - PUT
    - PATCH
    - DELETE

    Specify the required "role" using the role_required attribute.

    e.g.

    role_required = "part"

    The RoleMixin class will then determine if the user has the required permission
    to perform the specified action.

    For example, a DELETE action will be rejected unless the user has the "part.remove" permission
    """

    def has_permission(self, request, view):
        """
        Determines whether the current user is authorized to perform the requested action on the view.
        
        Superusers are granted access immediately. For other users, the HTTP request method is mapped to a
        permission type (e.g., view, add, change, delete) using a default mapping that can be overridden by the view.
        If the view specifies a required role (which can include an explicit permission using the syntax
        "role.permission"), the user's roles are checked accordingly. In the absence of an explicit role requirement,
        the method attempts to infer the target model from the view and builds a permission table name using the
        model’s app label and name; it then verifies that the user has the corresponding permission via the ruleset.
        If model metadata is unavailable, the method defaults to granting permission.
        
        Returns:
            bool: True if the user is authorized, False otherwise.
        """
        user = request.user

        # Superuser can do it all
        if user.is_superuser:
            return True

        # Map the request method to a permission type
        rolemap = {
            'GET': 'view',
            'OPTIONS': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete',
        }

        # let the view define a custom rolemap
        if hasattr(view, 'rolemap'):
            rolemap.update(view.rolemap)

        permission = rolemap[request.method]

        # The required role may be defined for the view class
        if role := getattr(view, 'role_required', None):
            # If the role is specified as "role.permission", split it
            if '.' in role:
                role, permission = role.split('.')

            return users.models.check_user_role(user, role, permission)

        try:
            # Extract the model name associated with this request
            model = get_model_for_view(view)

            if model is None:
                return True

            app_label = model._meta.app_label
            model_name = model._meta.model_name

            table = f'{app_label}_{model_name}'
        except AttributeError:
            # We will assume that if the serializer class does *not* have a Meta,
            # then we don't need a permission
            return True

        return users.models.RuleSet.check_table_permission(user, table, permission)


def map_scope(roles: Optional[list[str]] = None, only_read=False) -> dict:
    """
    Map HTTP request methods to their required permission scopes.
    
    This function returns a dictionary mapping common HTTP methods to the scopes needed
    for permission checks. If the only_read flag is True, every scope is set to require read
    access regardless of roles. Otherwise, if roles are provided, each action scope is combined
    with each role to form a pair [action, role]. If no roles are specified, a default scope with
    the action name alone is returned. The OPTIONS method always requires read access.
    
    Args:
        roles: Optional list of role identifiers used to build entity-specific scopes.
        only_read: If True, all actions will be mapped to read-only permission scopes.
    
    Returns:
        A dictionary with HTTP methods ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS')
        as keys and lists of required permission scopes (each represented as a list of strings)
        as values.
    """

    def scope_name(tables, action):
        """
        Constructs a scope specification list based on the given action and table names.
        
        If the global flag only_read is set, returns a read-only scope [['read']]. Otherwise,
        when tables are provided, returns a list of scopes pairing the action with each table; if
        tables is empty, returns a list containing a single scope with the action.
        """
        if only_read:
            return [['read']]
        if tables:
            return [[action, table] for table in tables]
        return [[action]]

    return {
        'GET': scope_name(roles, 'view'),
        'POST': scope_name(roles, 'add'),
        'PUT': scope_name(roles, 'change'),
        'PATCH': scope_name(roles, 'change'),
        'DELETE': scope_name(roles, 'delete'),
        'OPTIONS': [['read']],
    }


# Precalculate the roles mapping
roles = users.models.RuleSet.get_ruleset_models()
precalculated_roles = {}
for role, tables in roles.items():
    for table in tables:
        if table not in precalculated_roles:
            precalculated_roles[table] = []
        precalculated_roles[table].append(role)


class InvenTreeTokenMatchesOASRequirements(TokenMatchesOASRequirements):
    """Permission that discovers the required scopes from the OpenAPI schema."""

    def has_permission(self, request, view):
        """
        Determines if the request has valid permission.
        
        If the user is authenticated by any method other than OAuth2, permission is granted without further checks.
        For OAuth2-authenticated requests, the method defers to the superclass’s permission check (which verifies
        the required scopes).
        
        Returns:
            bool: True if the request has permission, False otherwise.
        """
        is_authenticated = permissions.IsAuthenticated().has_permission(request, view)
        oauth2authenticated = False
        if is_authenticated:
            oauth2authenticated = isinstance(
                request.successful_authenticator, OAuth2Authentication
            )

        return (is_authenticated and not oauth2authenticated) or super().has_permission(
            request, view
        )

    def get_required_alternate_scopes(self, request, view):
        """
        Return alternate OAuth2 scopes for the request based on the view's attributes.
        
        If the view defines a 'required_alternate_scopes' attribute, that value is returned.
        Otherwise, the function attempts to determine the model associated with the view via
        get_model_for_view. If a model is identified, it retrieves the corresponding roles from
        the precalculated mapping and computes the required scopes using map_scope. In cases
        where the model is absent or an error occurs, a read-only scope mapping is returned.
        """
        if hasattr(view, 'required_alternate_scopes'):
            return view.required_alternate_scopes
        try:
            # Extract the model name associated with this request
            model = get_model_for_view(view)

            if model is None:
                return map_scope(only_read=True)

            return map_scope(
                roles=precalculated_roles.get(
                    f'{model._meta.app_label}_{model._meta.model_name}', []
                )
            )
        except AttributeError:
            # We will assume that if the serializer class does *not* have a Meta,
            # then we don't need a permission
            return map_scope(only_read=True)
        except Exception:
            return map_scope(only_read=True)


class IsSuperuser(permissions.IsAdminUser):
    """Allows access only to superuser users."""

    def has_permission(self, request, view):
        """Check if the user is a superuser."""
        return bool(request.user and request.user.is_superuser)


class IsSuperuserOrReadOnly(permissions.IsAdminUser):
    """Allow read-only access to any user, but write access is restricted to superuser users."""

    def has_permission(self, request, view):
        """Check if the user is a superuser."""
        return bool(
            (request.user and request.user.is_superuser)
            or request.method in permissions.SAFE_METHODS
        )


class IsStaffOrReadOnly(permissions.IsAdminUser):
    """Allows read-only access to any user, but write access is restricted to staff users."""

    def has_permission(self, request, view):
        """Check if the user is a superuser."""
        return bool(
            (request.user and request.user.is_staff)
            or request.method in permissions.SAFE_METHODS
        )


def auth_exempt(view_func):
    """Mark a view function as being exempt from auth requirements."""

    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.auth_exempt = True
    return wraps(view_func)(wrapped_view)
