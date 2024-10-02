import random 
import logging


from django.db import models, transaction 
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token # type: ignore
from django_rest_passwordreset.signals import reset_password_token_created # type: ignore
from config_master import TZ, EMAIL_VERIFICATION_CODE_EXPIRY, COUNTIES_CHOICES, ROLE_CHOICES, ROLE_USER
from oneworld.models import BaseModel
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField # type: ignore



log = logging.getLogger(__name__)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
  send_mail().send_password_reset_email({'reset_password_token': reset_password_token})

class Address(BaseModel):
  """
  This class represents the address model that holds details of a user's address
  """
  address_line = models.CharField(max_length=1000, blank=True, null=True, default='')
  county = models.CharField(max_length=1000, blank=True, null=True, default='', choices=COUNTIES_CHOICES)
  city = models.CharField(max_length=1000, blank=True, null=True, default='')
  street = models.CharField(max_length=1000, blank=True, null=True, default='')
  is_verified = models.BooleanField(default=False)
  verification_code = models.PositiveIntegerField(default=0)
  
  
  def get_verification_code(self) -> int:
    """
    This method generates a verification code for a user's address. If the address is already verification code, it returned
    """
    if self.verification_code != 0:
      return self.verification_code
    self.verification_code = random.randint(100000, 999999)
    self.save()
    return self.get_verification_code()

class Profile(BaseModel):
  """ 
  This returns the profile of the user
  """
  user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
  role  = models.CharField(max_length=100, blank=True, null=True, default=ROLE_USER, choices=ROLE_CHOICES)
  phone = PhoneNumberField(blank=True, null=True)
  other_phone = PhoneNumberField(blank=True, null=True)
  
  def __str__(self):
    return '%s %s' % (self.user.first_name, self.user.role)
