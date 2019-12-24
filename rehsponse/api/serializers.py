from django.utils.timesince import timesince
from django.urls import reverse_lazy
from rest_framework import serializers
from rehsponse import models


class UserSimplified(serializers.ModelSerializer):
    """Public Display of user profile simplified"""
    user_url = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = [
            'id',
            'first_name',
            'last_name',
            'city',
            "username",
            'user_url',
        ]

    def get_user_url(self, obj):
        return reverse_lazy('userdetail', kwargs={'username': obj.username})


class RehsponseChildSerializer(serializers.ModelSerializer):
    """Serialization of Response item (Reply)"""
    user_profile = UserSimplified(read_only=True)
    timesince = serializers.SerializerMethodField()
    love_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Rehsponse
        fields = [
            'id',
            'user_profile',
            'rehsponse_text',
            'rehsponse_image',
            'love_count',
            'timesince',
            'created_on',
        ]

    def get_love_count(self, obj):
        return obj.loved.all().count()

    def get_timesince(self, obj):
        return timesince(obj.updated_on) + " ago"


class RehsponseDetailSerializer(serializers.ModelSerializer):
    """Serialization of Response item (Parent)"""
    user_profile = UserSimplified(read_only=True)
    love_count = serializers.SerializerMethodField()  # total love count for this post
    did_love = serializers.SerializerMethodField()  # the user did love already
    reply_count = serializers.SerializerMethodField()   # total reply count
    replying_to_id = serializers.IntegerField(required=False, allow_null=True)
    all_replies = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()     # custom date
    date_display = serializers.SerializerMethodField()  # custom date
    own_url = serializers.SerializerMethodField()       # view url

    class Meta:
        model = models.Rehsponse
        fields = [
            'replying_to_id',
            'id',
            'user_profile',
            'rehsponse_text',
            'rehsponse_image',
            'love_count',
            'did_love',
            'reply_count',
            'all_replies',
            'date_display',
            'timesince',
            'own_url',
        ]

    def get_all_replies(self, obj):
        if obj.is_replying_to:
            return RehsponseChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_replying_to:
            return obj.children().count()
        return 0

    def get_did_love(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated:
            if user in obj.loved.all():
                return True
        return False

    def get_love_count(self, obj):
        return obj.loved.all().count()

    def get_date_display(self, obj):
        return obj.updated_on.strftime("%b %d, %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.updated_on) + " ago"

    def get_own_url(self, obj):
        return reverse_lazy('detail', kwargs={'pk': obj.id})


class UserSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    user_url = serializers.SerializerMethodField()
    all_post = RehsponseDetailSerializer(many=True, read_only=True)
    all_responders = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "all_responders",
            "all_post",
            "password",
            "user_url",
        ]

        read_only_fields = [
            "date_of_birth",
            "phone",
        ]

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def get_user_url(self, obj):
        return reverse_lazy('userdetail', kwargs={'username': obj.username})

    def get_all_responders(self, obj):
        request = self.context.get("request")
        user = request.user
        self_post = models.Rehsponse.objects.filter(user_profile_id=user.id)
        post_reply = models.Rehsponse.objects.filter(user_profile_id=user.id).exclude(replying_to=None)
        print(post_reply)

        # from replies only take uniuqe user

        # if obj.all_post:
        #     return obj.children().count()
        return 0

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            # date_of_birth=validated_data['date_of_birth'],
            # short_bio=validated_data['short_bio'],
            # address=validated_data['address'],
            # city=validated_data['city'],
            # country=validated_data['country'],
            # phone=validated_data['phone'],
        )
        return user


# HASH TAGS ========================================================
class HashTagSerializer(serializers.ModelSerializer):
    """Serializer for HashTag"""
    tag_url = serializers.SerializerMethodField()

    class Meta:
        model = models.HashTag
        fields = "__all__"

    def get_tag_url(self, obj):
        return reverse_lazy('hashtag', kwargs={'hashtag': obj.tag})


# CONTACTS ========================================================
class ContactSerializer(serializers.ModelSerializer):
    """Contacts Serializer"""

    class Meta:
        model = models.Contact
        fields = "__all__"
