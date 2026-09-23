from rest_framework.permissions import BasePermission
from rest_framework.response import Response


class IsPostAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        return request.user == obj.author