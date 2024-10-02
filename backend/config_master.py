import os
import pytz
from eco.settings import TIME_ZONE


ROLE_VENDOR = 'VENDOR'

TZ = pytz.timezone(TIME_ZONE)

EMAIL_VERIFICATION_CODE_EXPIRY = 300