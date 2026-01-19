from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny   # ← AJOUTE CETTE LIGNE
from .serializers import RegisterSerializer

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # ← AJOUTE CETTE LIGNE

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "detail": "Utilisateur créé avec succès",
            "username": user.username
        }, status=status.HTTP_201_CREATED, headers=headers)