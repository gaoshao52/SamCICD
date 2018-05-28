from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=64, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class CodeServer(models.Model):
    '''代码库服务器'''
    title = models.CharField(max_length=64, unique=True, verbose_name="标题")
    url = models.URLField(max_length=64, verbose_name="gitLab服务器地址")
    person_token = models.CharField(max_length=64, unique=True, verbose_name="PERSON_TOKEN")
    myuser = models.ForeignKey("MyUser", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "GitLab服务器"

    def __str__(self):
        return self.title


class BuildTools(models.Model):
    '''代码编译'''
    name = models.CharField(max_length=32, unique=True, verbose_name="工程名称")
    shell_code = models.TextField(blank=True, null=True)
    # email = models.EmailField(blank=True, null=True)
    artifact = models.CharField(max_length=64, blank=True, null=True)
    codeserver = models.ForeignKey("CodeServer", on_delete=models.CASCADE)
    myuser = models.ForeignKey("MyUser", on_delete=models.CASCADE)


class BuildProjectAndBranch(models.Model):
    git_repo = models.URLField()
    branch = models.CharField(max_length=32)
    group = models.CharField(max_length=32)
    # name = models.CharField(max_length=32, blank=True, null=True)
    buildtool = models.ForeignKey("BuildTools", on_delete=models.CASCADE)
    myuser = models.ForeignKey("MyUser", on_delete=models.CASCADE)


    def __str__(self):
        return self.git_repo



