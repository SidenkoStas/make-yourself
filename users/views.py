from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


# User = get_user_model()
#
#
# class UserViewSet(mixins.CreateModelMixin,
#                   mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin,
#                   GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

