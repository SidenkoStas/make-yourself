from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializers
from .models import CustomUser
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.renderers import TemplateHTMLRenderer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers


class SignUpView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "users/signup.html"

    def get(self, request, *args, **kwargs):
        serializer = UserSerializers()
        return Response({"user_form": serializer})

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if not serializer.is_valid():
            return Response({"user_form": serializer})
        serializer.save()
        return redirect("common:index")


# class SignUpView(ListCreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializers
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = "users/signup.html"
#
#     def get(self, request, *args, **kwargs):
#         user_form = UserSerializers()
#         return Response({"user_form": user_form})
#
#
