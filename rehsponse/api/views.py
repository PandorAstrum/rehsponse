from django.db.models import Q
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView

from rehsponse.api import serializers, permission
from rehsponse import models
from rehsponse.api import pagination


# USER ACCOUNT ==================================================
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


class LoveToggleAPIView(APIView):
    """Love Toggle Endpoints"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        rehsponse_qs = models.Rehsponse.objects.filter(pk=pk)
        message = "Not Allowed"
        if request.user.is_authenticated:
            is_loved = models.Rehsponse.objects.love_toggle(request.user, rehsponse_qs.first())
            return Response({'loved': is_loved})
        return Response({'message': message}, status=400)


# REHSPONSES ====================================================
class RehsponseListAPIView(generics.ListAPIView):
    """Get all list of response (RETRIEVE ALL)"""
    # authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.RehsponseDetailSerializer
    pagination_class = pagination.StandardResultsPaginations

    def get_serializer_context(self, *args, **kwargs):
        context = super(RehsponseListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self):
        # get random response
        qs2 = models.Rehsponse.objects.filter(user_profile=self.request.user)
        qs3 = models.Rehsponse.objects.filter(replying_to_id=None)
        qs = (qs2 | qs3).distinct()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(rehsponse_text__icontains=query) |
                Q(user_profile__first_name__icontains=query) |
                Q(user_profile__last_name__icontains=query)
            )
        return qs


class RehsponseDetailAPIView(generics.RetrieveAPIView):
    """Get a single rehsponses (RETRIEVE SINGLE)"""
    # authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.RehsponseDetailSerializer
    queryset = models.Rehsponse.objects.all()


class RehsponseCreateAPIView(generics.CreateAPIView):
    """Create a response (CREATE)"""
    # authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.RehsponseDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)


class RehsponseUpdateAPIView(generics.UpdateAPIView):
    # authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.RehsponseDetailSerializer
    queryset = models.Rehsponse.objects.all()


class RehsponseDeleteAPIView(generics.DestroyAPIView):
    serializer_class = serializers.RehsponseDetailSerializer


class ContactListAPIView(generics.ListAPIView):
    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializer


# HASHTAGS ======================================================
class HashTagListAPIView(generics.ListAPIView):
    """Get all list of hash tags (RETRIEVE ALL) Limit to only 10 in negative date order"""
    serializer_class = serializers.HashTagSerializer

    def get_queryset(self):
        """Query mixin"""
        return models.HashTag.objects.all().order_by('-created_on')[:10]


class UserDetailAPIView(generics.RetrieveAPIView):
    """User Detail view"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self, queryset=models.UserProfile):
        _user_name = self.kwargs.get('username')
        obj = get_object_or_404(models.UserProfile, username__iexact=_user_name)
        return obj


class UserCreateAPIView(generics.CreateAPIView):
    """User Detail view"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self, queryset=models.UserProfile):
        _user_name = self.kwargs.get('username')
        obj = get_object_or_404(models.UserProfile, username__iexact=_user_name)
        return obj


class UserListAPIView(generics.ListAPIView):
    """User Detail view"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self, queryset=models.UserProfile):
        _user_name = self.kwargs.get('username')
        obj = get_object_or_404(models.UserProfile, username__iexact=_user_name)
        return obj


class PostViewSets(viewsets.ModelViewSet):
    """Handles Response from users"""
    serializer_class = serializers.RehsponseDetailSerializer
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
