from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from .validator import validate_response
from django.urls import reverse, reverse_lazy


# Create your models here.
class UserManager(BaseUserManager):
    """Manager for user profile"""

    def create_user(self, email, password=None, **extra_fields):
        """Create a user profile"""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create a super user"""
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database user profile model in the system"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    responded_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="responded_to")
    # username = first_name + last_name
    # gender = models.Choices
    short_bio = models.TextField(blank=True, null=True)
    # interest =
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    # user_image = models.ImageField()
    created_on = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.first_name

    def __str__(self):
        """String representation of user"""
        return self.email


# class UserProfile(models.Model):
#     # they response us
#     response_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="responded_to",
#                                         null=True)
#     # we response to them
#     response_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="responder")
#
#     def __str__(self):
#         return str(self.response_to.all().count())


class Rehsponse(models.Model):
    """Response Model  in the System"""
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='poster')
    rehsponse_text = models.TextField(max_length=140, validators=[validate_response])
    # post_image = models.ImageField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of profile post"""
        return self.rehsponse_text

    class Meta:
        ordering = ['-updated_on']

    def get_absolute_url(self, obj):
        return reverse_lazy("detail", kwargs={'pk': obj.pk})


class HashTag(models.Model):
    tag = models.CharField(max_length=120)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def get_rehsponse(self):
        return Rehsponse.objects.filter(rehsponse_text__icontains="#" + self.tag)

    # def get_absolute_url(self):
    #     return reverse_lazy("hashtag", kwargs={'hashtag': self.tag})


class Contact(models.Model):
    title_text = models.CharField(max_length=255)
    content_text = models.TextField(blank=True, null=True)
    icon_name = models.CharField(max_length=120, default="fas fa-5x fa-stack-1x fa-book-open")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title_text
