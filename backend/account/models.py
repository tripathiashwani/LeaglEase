import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import RegexValidator


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    phone=models.CharField(validators=[phone_regex], max_length=17,blank=True, null=True,default=9876546210)
    objects = CustomUserManager()
    


class Case(models.Model):
    CASE_TYPES = (
        ('civil', 'Civil'),
        ('criminal', 'Criminal'),
        ('family', 'Family'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_of_case = models.CharField(max_length=20, choices=CASE_TYPES)
    clients = models.ManyToManyField(CustomUser, related_name='cases_as_client')
    mediator = models.ForeignKey('Mediator', on_delete=models.SET_NULL, null=True, blank=True, related_name='mediated_cases')
    
    def __str__(self):
        return f"Case {self.id} - {self.type_of_case}"



class Mediator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    rating = models.FloatField(default=0.0)
    cases = models.ManyToManyField(Case, related_name='active_mediators', blank=True)
    history = models.ManyToManyField(Case, related_name='mediator_history', blank=True)
    docs = models.FileField(upload_to='lawyer_docs/', blank=True, null=True)
    
    def __str__(self):
        return f"Mediator {self.user.username}"


class Lawyer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    docs = models.FileField(upload_to='lawyer_docs/', blank=True, null=True)
    current_cases = models.ManyToManyField(Case, related_name='lawyers', blank=True)
    
    def __str__(self):
        return f"Lawyer {self.user.username}"



class PhoneOTP(models.Model):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)

    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')

    def __str__(self):
        return str(self.otp)
    


class Notification(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(CustomUser, related_name='received_notification', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, related_name='created_notification', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SENT)


class Meeting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, related_name='meetings', on_delete=models.CASCADE)
    mediator = models.ForeignKey(Mediator, related_name='meetings', on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.DurationField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, related_name='created_meetings', on_delete=models.CASCADE)
    attendees = models.ManyToManyField(CustomUser, related_name='meetings', blank=True)
    status = models.CharField(max_length=20, choices=Notification.STATUS_CHOICES, default=Notification.SENT)