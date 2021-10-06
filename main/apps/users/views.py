from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from main.apps.core.swagger import path_id_param_str
from .models import User
from .permissions import IsUserOwner
from .serializers import UserSerializer


@method_decorator(name='retrieve', decorator=path_id_param_str)
@method_decorator(name='update', decorator=path_id_param_str)
@method_decorator(name='partial_update', decorator=path_id_param_str)
class UserViewSets(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    queryset = User.objects.active()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwner]

    def get_queryset(self):
        return super(UserViewSets, self).get_queryset().owner(self.request.user)

    @action(methods=['get', 'patch', 'put'], detail=False)
    def self(self, request, *args, **kwargs):
        self.kwargs.update({'pk': self.get_queryset().first().id})
        if request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
        elif request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        else:
            return self.retrieve(request, *args, **kwargs)

