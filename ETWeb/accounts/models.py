from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, username, password, *,
                    email=None, is_staff=False, is_superuser=False,
                    is_active=False, date_joined=None):
        if not username:
            raise ValueError("Username field must have a username.")
        if not password:
            raise ValueError("Username field must have a password.")

        user_obj = self.model(username=username)
        user_obj.set_password(password)  # change password
        user_obj.email = self.normalize_email(email)
        user_obj.is_staff = is_staff
        user_obj.is_superuser = is_superuser
        user_obj.is_active = is_active
        user_obj.date_joined = date_joined
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, username, password, **kwargs):
        return self.create_user(username, password, is_superuser=True, is_staff=True, is_active=True, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=60)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # cannot login by default
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    objects = UserManager()

    @property
    def profile(self):
        obj, created = UserProfile.objects.get_or_create(user=self)
        return obj

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = "accounts_users"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def wrap_user_creation(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        UserProfile.objects.create(user=instance)


class UserProfile(models.Model):
    DEFAULT_PROFILE_IMAGE = 'profile_images/default_user_image.jpg'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True, default='John')
    last_name = models.CharField(max_length=100, null=True, blank=True, default='Doe')
    company = models.CharField(max_length=100, null=True, blank=True, default='Unemployed')
    current_position = models.CharField(max_length=100, null=True, blank=True, default='Unemployed')
    image = models.ImageField(upload_to='profile_images',
                              default=DEFAULT_PROFILE_IMAGE,
                              blank=True)

    @property
    def full_name(self):
        if not (self.first_name or self.last_name):
            return self.user.username
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "accounts_userprofiles"

