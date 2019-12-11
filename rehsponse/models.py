from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from .validator import validate_response
from django.urls import reverse


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
    # GENDER_CHOICES = (
    #     (1, 'Male'),
    #     (2, 'Female'),
    # )
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    # username = first_name + last_name
    # gender = models.Choices
    short_bio = models.TextField(blank=True, null=True)
    # interest =
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
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


class Rehsponse(models.Model):
    """Response Model  in the System"""
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rehsponse_text = models.TextField(max_length=140, validators=[validate_response])
    # post_image = models.ImageField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of profile post"""
        return self.rehsponse_text

    # def get_absolute_url(self):
    #     return reverse('rehsponse.views.RehsponseDetailView', args=[str(self.id)])
