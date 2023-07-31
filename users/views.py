from rest_framework.generics import CreateAPIView
from .serializers import UserSerializers
from .models import CustomUser


class SignUpView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers
