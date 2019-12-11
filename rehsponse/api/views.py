from django.db.models import Q
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rehsponse.api import serializers, permission
from rehsponse import models


# Create your views here.
class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileViewSets(viewsets.ModelViewSet):
    """Handle creating, updating, deleting user profiles"""
    serializer_class = serializers.UserSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name', 'email', )


class UserPasswordChange():
    """Handles request for password change"""
    pass


class RehsponseListView(generics.ListAPIView):
    serializer_class = serializers.RehsponseSerializer

    def get_queryset(self):
        qs = models.Rehsponse.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(rehsponse_text__icontains=query) |
                Q(user_profile__first_name__icontains=query) |
                Q(user_profile__last_name__icontains=query)
            )
        return qs


class PostViewSets(viewsets.ModelViewSet):
    """Handles Response from users"""
    serializer_class = serializers.RehsponseSerializer
    queryset = models.Rehsponse.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permission.UpdateOwnPost,
        IsAuthenticated
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('post_text', )

    def perform_create(self, serializer):
        """Sets the user profile to the looged in user"""
        serializer.save(user_profile=self.request.user)