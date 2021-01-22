from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        elif obj.collaborator == request.user:
            return True
        else:
            return False

class IsCollaborator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        collaborators = []
        collaborators = obj.collaborator.all()
        if collaborators:
            for collaborator in collaborators:
                if collaborator == request.user:
                    return True
        elif obj.owner == request.user:
            return True
        else:
            return False
