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
    serializer_class = serializers.RehsponseDetailSerializer
    pagination_class = pagination.StandardResultsPaginations
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def get_serializer_context(self, *args, **kwargs):
        context = super(RehsponseListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self):
        # get random response
        qs2 = models.Rehsponse.objects.filter(user_profile=self.request.user)
        qs3 = models.Rehsponse.objects.filter(replying_to=None)
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
    serializer_class = serializers.RehsponseDetailSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    queryset = models.Rehsponse.objects.all()


class RehsponseCreateAPIView(generics.CreateAPIView):
    """Create a response (CREATE)"""
    serializer_class = serializers.RehsponseDetailSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)


class RehsponseUpdateAPIView(generics.UpdateAPIView):
    """Edit a rehsponse (UPDATE)"""
    serializer_class = serializers.RehsponseDetailSerializer
    permission_classes = (IsAuthenticated, permission.UpdateOwnPost)
    # authentication_classes = (TokenAuthentication,)
    queryset = models.Rehsponse.objects.all()


class RehsponseDeleteAPIView(generics.DestroyAPIView):
    """Delete a rehsponse (DESTROY)"""
    serializer_class = serializers.RehsponseDetailSerializer
    permission_classes = (IsAuthenticated, permission.UpdateOwnPost)
    # authentication_classes = (TokenAuthentication,)


class ContactListAPIView(generics.ListAPIView):
    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializer


# HASHTAGS ======================================================
class HashTagListAPIView(generics.ListAPIView):
    """Get all list of hash tags (RETRIEVE ALL) Limit to only 10 in negative date order"""
    serializer_class = serializers.HashTagSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        """Query mixin"""
        return models.HashTag.objects.all().order_by('-created_on')[:10]


# USERS =========================================================
class UserDetailAPIView(generics.RetrieveAPIView):
    """User Detail view (RETRIEVE SINGLE)"""
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def get_serializer_context(self, *args, **kwargs):
        context = super(UserDetailAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_object(self, queryset=models.UserProfile):
        _user_name = self.kwargs.get('user_name')
        obj = get_object_or_404(models.UserProfile, user_name__iexact=_user_name)
        return obj

    def get_queryset(self):
        user = self.request.user.id
        return models.UserProfile.objects.filter(id=user)


class UserCreateAPIView(generics.CreateAPIView):
    """Create a user (CREATE)"""
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=models.UserProfile):
        _user_name = self.kwargs.get('user_name')
        obj = get_object_or_404(models.UserProfile, user_name__iexact=_user_name)
        return obj


class UserEditAPIView(generics.UpdateAPIView):
    """Edit a User (UPDATE)"""
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, permission.UpdateOwnProfile)
    # authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=models.UserProfile):
        _user_name = self.kwargs.get('user_name')
        obj = get_object_or_404(models.UserProfile, user_name__iexact=_user_name)
        return obj


class UserDeleteAPIView(generics.DestroyAPIView):
    """Delete a User (Destroy)"""
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, permission.UpdateOwnProfile)
    # authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=models.UserProfile):
        _user_name = self.kwargs.get('user_name')
        obj = get_object_or_404(models.UserProfile, user_name__iexact=_user_name)
        return obj
