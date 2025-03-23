import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields,
        )

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(
        max_length=255,
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        editable=False
    )
    email = models.EmailField(
        verbose_name=_("email"),
        unique=True
    )
    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=150,
        null=True,
        blank=False
    )
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=150,
        null=True,
        blank=False
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        auto_now=True
    )
    level = models.IntegerField(
        verbose_name=("level"),
        blank=True,
        null=True,
        default=0
    )
    contact_address = models.CharField(
        verbose_name=("contact_address"),
        max_length=150,
        null=True,
        blank=True,
    ) 

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email