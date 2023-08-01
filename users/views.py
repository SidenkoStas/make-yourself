from rest_framework.generics import ListCreateAPIView, CreateAPIView
from .serializers import UserSerializers
from .models import CustomUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer, HTMLFormRenderer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,

                  GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers
    # renderer_classes = [HTMLFormRenderer]


class SignUpView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers
    renderer_classes = [HTMLFormRenderer]
    template_name = "users/signup"
