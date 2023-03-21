"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manges User class."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError(('User must have an email address.'))
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a super user."""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model for creating User for authentication and creating blogs.

    Attribs:
        email (str): Email of the user.
        name (str): Name of the user.
        is_active (bool): Whether user is active or not.
        is_staff (bool): Whether user is a staff or not.
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """
    Model for creating recipe.

    Attribs:
        user (obj): Author of the recipe.
        title (str): Title of the recipe.
        description (str): Description of the recipe.
        time_minutes (datetime): Time taken to cook the recipe.
        price (float): Price required to pay for the recipe.
        link (str): Link of the recipe.


    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag',)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Model for creating Tag for filtering recipies.

    Attribs:
        name (str): Name of the tag.
        user (obj): User who has created the tag.
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
