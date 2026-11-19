from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator , MaxLengthValidator
from django.utils import timezone
import django.core.exceptions.ValidationError

# Create your models here.
class User(AbstractUser):
    pass
class Doctor(User):
    license_number = models.CharField(max_length=6, unique=True, validators=[RegexValidator(regex=r'^[A-Za-z0-9]{6}$', message='License number must be exactly 6 alphanumeric characters.')])
    phone = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    speciality = models.ManyToManyField('speciality', related_name='doctors')
    number_of_appointments = models.PositiveIntegerField(default=0)
    number_validator = RegexValidator(
    regex=r'^\d{8}$',
    message="Number must be 8 digits "
    )
def validate_birth_date(v):
    if v > timezone.now().date():
        raise ValidationError("Birth date cannot be in the future.")
class patient(User):
    national_id = models.CharField(max_length=8, unique=True, validators=[MinLengthValidator(8), MaxLengthValidator(8)])
    phone = models.CharField(max_length=8)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class speciality(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

