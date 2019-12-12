from django.db.models import Q
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rehsponse.api import serializers, permission
from rehsponse import models
from rehsponse.api import pagination


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

# user detail view
# class UserDetailAPIView(generics.Deta)
class UserPasswordChange():
    """Handles request for password change"""
    pass


# list response
class RehsponseListAPIView(generics.ListAPIView):
    """Get all list of response"""
    serializer_class = serializers.RehsponseSerializer
    pagination_class = pagination.StandardResultsPaginations

    def get_queryset(self):
        qs = models.Rehsponse.objects.all().order_by('-updated_on')
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(rehsponse_text__icontains=query) |
                Q(user_profile__first_name__icontains=query) |
                Q(user_profile__last_name__icontains=query)
            )
        return qs


# create response
class RehsponseCreateAPIView(generics.CreateAPIView):
    """Create a response"""
    serializer_class = serializers.RehsponseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)


# retrieve
class RehsponseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.RehsponseSerializer
    queryset = models.Rehsponse.objects.all()


# update
class RehsponseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.RehsponseSerializer
    queryset = models.Rehsponse.objects.all()


# delete
class RehsponseDeleteAPIView(generics.DestroyAPIView):
    serializer_class = serializers.RehsponseSerializer


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