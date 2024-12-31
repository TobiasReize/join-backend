from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]     # wenn man sich registrieren möchte, ist man noch nicht authentisiert! (daher AllowAny)

    def post(self, request):    # Funktion wird nur bei einem POST-Request ausgeführt!
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()     # Rückgabewert der save-Methode wird gespeichert! (ist das neue User-Objekt/ Account)
            token, created = Token.objects.get_or_create(user=saved_account)     # hier wird der Auth-Token für den neuen User erstellt! (es wird ein Tupel zurückgegeben!)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email
            }
        else:
            data = serializer.errors
        return Response(data)


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):    # Funktion wird nur bei einem POST-Request ausgeführt!
        serializer = self.serializer_class(data=request.data)   # es wird der Serializer von der Django-View "ObtainAuthToken" verwendet!
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']    # der bestehende User wird gezogen!
            token, created = Token.objects.get_or_create(user=user)     # Falls ein User noch kein Token hat, wird er hier erstellt! (es wird ein Tupel zurückgegeben!)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email
            }
        else:
            data = serializer.errors

        return Response(data)
