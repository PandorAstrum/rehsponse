from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .validator import validate_response
from django.urls import reverse_lazy


def upload_location(instance, filename):
    _model = instance.__class__
    new_id = _model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


class UserManager(BaseUserManager):
    """Manager for user profile"""
    def create_user(self, email, user_name, password=None, **extra_fields):
        """Create a user profile"""
        if not email:
            raise ValueError("User must have an email address")
        if not user_name:
            raise ValueError("User must enter a username.")

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password, **extra_fields):
        """Create a super user"""
        user = self.create_user(email, user_name, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database user profile model in the system"""
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    user_name = models.CharField(max_length=255, unique=True)
    short_bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    user_image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field",
    )
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.first_name

    def get_email(self):
        """Retrieve email of user"""
        return self.email

    def __str__(self):
        """String representation of user"""
        return self.user_name


class RehsponseManager(models.Manager):
    """manager object for rehsponse"""
    def from_user(self, user):
        return self.get_query_set().filter(user_profile_id=user.id)

    def respond(self, user, replying_to_obj):
        if replying_to_obj.replying_to:
            original_ = replying_to_obj.replying_to
        else:
            original_ = replying_to_obj

        obj = self.model(
            replying_to=original_,
            user_profile=user,
            rehsponse_text=original_.rehsponse_text
        )

        obj.save()
        return obj

    def love_toggle(self, user, response_obj):
        if user in response_obj.loved.all():
            is_loved = False
            response_obj.loved.remove(user)
        else:
            is_loved = True
            response_obj.loved.add(user)
        return is_loved


class Rehsponse(models.Model):
    """Rehsponse Model in the System"""
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='all_post')
    rehsponse_text = models.TextField(max_length=140, validators=[validate_response])
    rehsponse_image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field"
    )
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    loved = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="loved_by")
    replying_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = RehsponseManager()

    def __str__(self):
        """String representation of profile post"""
        return self.rehsponse_text

    class Meta:
        ordering = ['-updated_on']

    def get_absolute_url(self):
        return reverse_lazy("detail", kwargs={'pk': self.pk})

    def children(self):  # replies
        return Rehsponse.objects.filter(replying_to=self)

    @property
    def is_replying_to(self):
        if self.replying_to is not None:
            return False
        return True


class HashTag(models.Model):
    """Hash Tag Model in the system"""
    tag = models.CharField(max_length=120)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def get_rehsponse(self):
        return Rehsponse.objects.filter(rehsponse_text__icontains="#" + self.tag)

    # def get_absolute_url(self):
    #     return reverse_lazy("hashtag", kwargs={'hashtag': self.tag})


class Contact(models.Model):
    """Dynamic Contact Page model"""
    title_text = models.CharField(max_length=255)
    content_text = models.TextField(blank=True, null=True)
    icon_name = models.CharField(max_length=120, default="fas fa-5x fa-stack-1x fa-book-open")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title_text
