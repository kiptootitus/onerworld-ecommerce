import random 
import logging


from django.db import models, transaction 
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from config_master import TZ, EMAIL_VERIFICATION_CODE_EXPIRY
from oneworld.models import BaseModel
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField



log = logging.getLogger(__name__)
