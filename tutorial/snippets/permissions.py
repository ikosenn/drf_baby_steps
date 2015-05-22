from rest_framework import permissions

class IsOwnwerOrReadOnly(permissions.BasePermission):
    '''
    Custom permission to only allow owners of an object
    to edit it
    '''
    def has_object_permission(self, request, view, obj):
        #read permissions are allowed to any request
        #just allo GET,HEAD ir OPTION requests
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user