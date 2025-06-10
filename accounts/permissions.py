from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, req, view): return req.user.role == req.user.ADMIN
