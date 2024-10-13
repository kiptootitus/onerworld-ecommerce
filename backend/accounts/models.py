import random 
import logging

from django.db import models, transaction
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.cache import cache
from django_rest_passwordreset.signals import reset_password_token_created
from config_master import EMAIL_VERIFICATION_CODE_EXPIRY, COUNTIES_CHOICES, ROLE_CHOICES, ROLE_USER
from oneworld.models import BaseModel
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from django.db.models.signals import post_save

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
    return '%s %s' % (self.user.first_name, self.user.role) # returns first name and replace with the first '%s then the second '%s' with the role


class ProfileAddress(Address):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_address')
  is_default = models.BooleanField(default=False)
  title = models.CharField(max_length=500, null=True, blank=True)
  house_number = models.CharField(max_length=500, null=True, blank=True)
  building_name = models.CharField(max_length=500, null=True, blank=True)
  landmark = models.CharField(max_length=500, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(instance, sender, created, **kwargs):
  """
  This is a signal that is called when creating a user object, and it creates a profile for the new user.
  If the user is being updated, then the profile is not created.
  :param sender:
  :param instance: The user object that is being created
  :param created: Boolean value that indicates whether the user object is being created or updated
  :param kwargs:
  :return: None
  """
  if created:
    Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  """
  This signal that is called when saving a user object.
  """
  Profile.objects.get(user=instance).save()

class AccountManger:

  def get_profile_address(self, data):
    """
    This method returns the default profile address of a user
    :param data: {
        'user': The user object
    }
    :return:
    """
    user = data.get('user')
    if user.profile.profile_address.all():
      if user.profile.profile_address.filter(is_default=True):
        return user.profile.profile_address.filter(is_default=True).first()
      return user.profile.profile_address.all.order_by('is_create_datetime').first()
  def get_user_by_email(self, data: dict) -> User or None:
    if User.objects.fileter(username=data.get('email')):
      return User.objects.get(username=data.get('email'))

  def get_all_users(self) -> User.objects:
    """
    This method returns all the users
    :return: User.objects
    """
    return User.objects.all()

  def create_update_vendor(self, data: dict) -> User:
    """
    This method creates or updates a vendor object
    :param data: {
        'email': The username of the vendor
        'password': The password of the vendor
        'role: The user role
    }
    :return:
    """
    with transaction.atomic():
      user = self.create_update_user(data)
      from vendor.models import VendorManager
      VendorManager().create_update_vendor_by_user({
        'user': user,
      })
      return user

  def create_update_user(self, data: dict) -> User:
    """
    This method creates or updates a vendor object
    :param data: {
        'email': The username of the vendor
        'password': The password of the vendor
        'role: The user role
        'first_name: The first name
        'last_name: The last name
        'phone_number: The phone number
    }
    :return:
    """
    with transaction.atomic():
      if User.objects.filter(username=data.get('email')).exists():
        user = User.objects.filter(username=data.get('email')).last()
      else:
        user = User()
        user.is_active = False
      user.username = data.get('email')
      user.first_name = data.get('first_name', '')
      user.last_name = data.get('last_name', '')
      user.email = data.get('email')
      user.set_password(data.get('password'))
      user.save()
      profile = user.profile
      profile.role = data.get('role')
      profile.phone = data.get('phone_number')
      profile.save()
      return user

  def generate_otp_for_email(self, email) -> int:
    """
    This method generates an OTP for the phone number, sets it to cache and returns it
    :param email: The email of the user
    :return:
    """
    otp = random.randint(100000, 999999)
    cache.set(email, otp, timeout=EMAIL_VERIFICATION_CODE_EXPIRY)
    return otp

  def verify_email_verification_code(self, email, code):
    """
    This function verifies the password reset code
    :param email: The email of the user
    :param code: The code to be verified
    :return:
    """
    if cache.get(email) == int(code):
      return True
    return False

  def change_user_status(self, email, status: bool) -> User:
    """
    This method sets user status to true or False
    :param email: The email of the user
    :param status: The value of the status
    :return: User
    """
    user = User.objects.get(username=email)
    user.is_active = status
    user.save()
    return user

  def create_address(self, data: dict) -> Address:
    """
    This method creates an address object
    :param data: {
        'address_line': The address line,
        'province': The province,
        'city': The city value,
        'street': The street value,
        'created_by': The created by value
    }
    :return: Address
    """
    return Address.objects.create(
      address_line=data.get('address_line'),
      province=data.get('province'),
      city=data.get('city'),
      street=data.get('street', ''),
      created_by=data.get('created_by'),
    )

  def get_all_addresses(self):
    """
    This method returns all the address objects
    :return:
    """
    return Address.objects.all()

  def verify_address(self, data: dict) -> True or False:
    """
    This method verify a particular address
    :param data: {
        'address_id': The ID value of the address,
        'verification_code': The verification code of the address,
    }
    :return: Address
    """
    address = Address.objects.get(id=data.get('address_id'))
    if str(address.verification_code) == str(data.get('verification_code')):
      address.is_verified = True
      address.verification_code = 0
      address.save()
      return True
    return False

  def create_profile_address(self, data: dict):
    """
    This method creates a new profile address for a user
    :param data: {
        'title':'',
        'first_name':'',
        'last_name':'',
        'phone':'',
        'other_phone':'',
        'house_number':'',
        'building_name':'',
        'landmark':'',
        'province':'',
        'city':'',
        'street':'',
        'user':''
    }
    :return:
    """
    user = data.get('user')
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.save()
    profile = user.profile
    profile.phone = data.get('phone')
    profile.other_phone = data.get('other_phone')
    profile.save()
    return ProfileAddress.objects.create(
      profile=profile,
      title=data.get('title'),
      house_number=data.get('house_number'),
      building_name=data.get('building_name'),
      landmark=data.get('landmark'),
      city=data.get('city'),
      street=data.get('street'),
      province=data.get('province'),
      created_by=data.get('created_by'),
    )

  def get_all_profile_address_of_user(self, data: dict):
    """
    This method returns all the profile address objects of a user
    :param data: {
        'user': The user object
    }
    :return:
    """
    user = data.get('user')
    return ProfileAddress.objects.filter(profile=user.profile)

  def fetch_account(self, user):
    """
    This method fetches the account of the user.
    :param user:
    :return:
    """
    return {'contact': str(user.profile.phone) if user.profile.phone else '',
            'other_phone': str(user.profile.other_phone) if user.profile.other_phone else '',
            'firstname': user.first_name,
            'last_name': user.last_name,
            }

  def fetch_contact(self, user):
    """
    This method fetches the contact details of the user.
    :param user:
    :return:
    """

    return user.profile.phone




