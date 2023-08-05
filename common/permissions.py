from rest_framework import permissions

from common import exceptions


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_anonymous:
            if user.is_blocked:
                raise exceptions.UnprocessableEntityException(
                    detail={
                        "title": "Account Blocked",
                        "message": "Accout Blocked",
                    },
                    code=417,
                )
            if not user.is_active:
                raise exceptions.UnprocessableEntityException(
                    detail={
                        "title": "Account Inactive",
                        "message": "Account Not Active",
                    },
                    code=406,
                )
            return True
        raise exceptions.UnprocessableEntityException(
            detail={
                "title": "UnAuthenticated",
                "message": "Not Authenticated",
            },
            code=401,
        )

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    The user is authenticated as a user or is a read-only request.
    """

    def has_permission(self, request, view):
        flag = bool(
            request.method in permissions.SAFE_METHODS
            or (request.user and request.user.is_authenticated)
        )
        if not flag:
            raise exceptions.UnprocessableEntityException(
                detail={
                    "title": "Authenticated",
                    "message": f"Not Authenticated for {request.method} request",
                },
                code=401,
            )
        return flag


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        flag = False
        try:
            flag = bool(request.user.role == "A")
        except:
            pass
        if not flag:
            raise exceptions.UnprocessableEntityException(
                detail={
                    "title": "Unauthenticated",
                    "message": "Not authenticated for admin request",
                },
                code=401,
            )
        return flag

    def has_object_permission(self, request, view, obj):
        return True


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        flag = False
        try:
            flag = bool(request.user.role == "SA")
        except:
            pass
        if not flag:
            raise exceptions.UnprocessableEntityException(
                detail={
                    "title": "Unauthenticated",
                    "message": "Not authenticated for superadmin request",
                },
                code=401,
            )
        return flag

    def has_object_permission(self, request, view, obj):
        return True


class IsSuperAdminOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        flag = False
        try:
            flag = bool(request.user.role == "A" or request.user.role == "SA")
        except:
            pass
        if not flag:
            raise exceptions.UnprocessableEntityException(
                detail={
                    "title": "Unauthenticated",
                    "message": "Not authenticated for super admin request",
                },
                code=401,
            )
        return flag

    def has_object_permission(self, request, view, obj):
        return True


class IsIntern(permissions.BasePermission):
    def has_permission(self, request, view):
        flag = False
        try:
            flag = bool(request.user.role == "I")
        except:
            pass
        if not flag:
            raise exceptions.UnprocessableEntityException(
                detail={
                    "title": "Unauthenticated",
                    "message": "Not authenticated for Intern request",
                },
                code=401,
            )
        return flag

    def has_object_permission(self, request, view, obj):
        return True


class IsSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        flag = False
        try:
            flag = bool(request.user.role == "S")
        except:
            pass
        if not flag:
            raise exceptions.UnprocessableEntityException(
                detail={
                    "title": "Unauthenticated",
                    "message": "Not authenticated for supervisor request",
                },
                code=401,
            )
        return flag

    def has_object_permission(self, request, view, obj):
        return True


class IsHumanResource(permissions.BasePermission):
    def has_permission(self, request, view):
        flag = False
        try:
            flag = bool(request.user.role == "HR")
        except:
            pass
        if not flag:
            raise exceptions.UnprocessableEntityException(
                detail={
                    "title": "Unauthenticated",
                    "message": "Not authenticated for human resource request",
                },
                code=401,
            )
        return flag

    def has_object_permission(self, request, view, obj):
        return True


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)

        return decorated_func

    return decorator


class IsInternOrSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        flag = False
        try:
            flag = bool(request.user.role == "S" or request.user.role == "I")
        except:
            pass
        if not flag:
            raise exceptions.UnprocessableEntityException(
                detail={
                    "title": "Unauthenticated",
                    "message": "Not authenticated for HR Supervisor request",
                },
                code=401,
            )
        return flag

    def has_object_permission(self, request, view, obj):
        return True
