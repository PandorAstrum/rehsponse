from django.utils.timesince import timesince
from django.urls import reverse_lazy
from rest_framework import serializers
from rehsponse import models


class UserDisplaySerializer(serializers.ModelSerializer):
    """Public Display of user profile"""
    rehsponder_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    user_url = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = [
            'first_name',
            'last_name',
            'city',
            'user_url',
            'rehsponder_count',
            'post_count'
        ]

    def get_rehsponder_count(self, obj):
        return 0

    def get_user_url(self, obj):
        return reverse_lazy('userdetail', kwargs={'username': obj.first_name})

    def get_post_count(self, obj):
        return 0


class RehsponseSerializer(serializers.ModelSerializer):
    """Serialization of Response item"""
    user_profile = UserDisplaySerializer(read_only=True)
    timesince = serializers.SerializerMethodField()
    date_display = serializers.SerializerMethodField()
    own_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Rehsponse
        fields = [
            'id',
            'user_profile',
            'rehsponse_text',
            'updated_on',
            'created_on',
            'date_display',
            'timesince',
            'own_url'
        ]

    def get_date_display(self, obj):
        return obj.updated_on.strftime("%b %d, %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.updated_on) + " ago"

    def get_own_url(self, obj):
        return reverse_lazy('detail', kwargs={'pk': obj.id})


class RehsponseSimpleSerializer(serializers.ModelSerializer):
    date_display = serializers.SerializerMethodField()
    own_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Rehsponse
        fields = [
            'id',
            'rehsponse_text',
            'updated_on',
            'date_display',
            'own_url'
        ]

    def get_date_display(self, obj):
        return obj.updated_on.strftime("%b %d, %I:%M %p")

    def get_own_url(self, obj):
        return reverse_lazy('detail', kwargs={'pk': obj.id})


class UserSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    user_url = serializers.SerializerMethodField()
    poster = RehsponseSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = models.UserProfile
        fields = "__all__"
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def get_user_url(self, obj):
        return reverse_lazy('userdetail', kwargs={'username': obj.first_name})

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            date_of_birth=validated_data['date_of_birth'],
            short_bio=validated_data['short_bio'],
            address=validated_data['address'],
            city=validated_data['city'],
            country=validated_data['country'],
            phone=validated_data['phone'],
        )
        return user


class ContactSerializer(serializers.ModelSerializer):
    """Contacts Serializer"""

    class Meta:
        model = models.Contact
        fields = "__all__"


class HashTagSerializer(serializers.ModelSerializer):
    """Serializer for HashTag"""
    tag_url = serializers.SerializerMethodField()

    class Meta:
        model = models.HashTag
        fields = "__all__"

    def get_tag_url(self, obj):
        return reverse_lazy('hashtag', kwargs={'hashtag': obj.tag})
