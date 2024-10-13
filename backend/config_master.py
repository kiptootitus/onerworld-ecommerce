import os
import pytz
from eco.settings import TIME_ZONE


ROLE_VENDOR = 'VENDOR'

TZ = pytz.timezone(TIME_ZONE)

EMAIL_VERIFICATION_CODE_EXPIRY = 300

COUNTIES_CHOICES=(
    ('COUNTY_Bomet', 'COUNTY_BOMET.title()'),
    ('COUNTY_Bungoma', 'COUNTY_BUNGOMA.title()'),
    ('COUNTY_Busia', 'COUNTY_BUSIA.title()'),
    ('COUNTY_Elgeyo_Marakwet', 'COUNTY_ELGEYO_MARAKWET.title()'),
    ('COUNTY_Embu', 'COUNTY_EMBU.title()'),
    ('COUNTY_Garissa', 'COUNTY_GARISSA.title()'),
    ('COUNTY_Homa_Bay', 'COUNTY_HOMA_BAY.title()'),
    ('COUNTY_Isiolo', 'COUNTY_ISIOLO.title()'),
    ('COUNTY_Kajiado', 'COUNTY_KAJIADO.title()'),
    ('COUNTY_Kakamega', 'COUNTY_KAKAMEGA.title()'),
    ('COUNTY_Kericho', 'COUNTY_KERICHO.title()'),
    ('COUNTY_Kiambu', 'COUNTY_KIAMBU.title()'),
    ('COUNTY_Kilifi', 'COUNTY_KILIFI.title()'),
    ('COUNTY_Kirinyaga', 'COUNTY_KIRINYAGA.title()'),
    ('COUNTY_Kisii', 'COUNTY_KISII.title()'),
    ('COUNTY_Kisumu', 'COUNTY_KISUMU.title()'),
    ('COUNTY_Kitui', 'COUNTY_KITUI.title()'),
    ('COUNTY_Laikipia', 'COUNTY_LAIKIPIA.title()'),
    ('COUNTY_Lamu', 'COUNTY_LAMU.title()'),
    ('COUNTY_Machakos', 'COUNTY_MACHAKOS.title()'),
    ('COUNTY_Makueni', 'COUNTY_MAKUENI.title()'),
    ('COUNTY_Mandera', 'COUNTY_MANDERA.title()'),
    ('COUNTY_Marsabit', 'COUNTY_MARSABIT.title()'),
    ('COUNTY_Meru', 'COUNTY_MERU.title()'),
    ('COUNTY_Migori', 'COUNTY_MIGORI.title()'),
    ('COUNTY_Mombasa', 'COUNTY_MOMBASA.title()'),
    ('COUNTY_Murang\'a', 'COUNTY_MURANG_A.title()'),
    ('COUNTY_Nairobi', 'COUNTY_NAIROBI.title()'),
    ('COUNTY_Nakuru', 'COUNTY_NAKURU.title()'),
    ('COUNTY_Nandi', 'COUNTY_NANDI.title()'),
    ('COUNTY_Narok', 'COUNTY_NAROK.title()'),
    ('COUNTY_Nyamira', 'COUNTY_NYAMIRA.title()'),
    ('COUNTY_Nyandarua', 'COUNTY_NYANDARUA.title()'),
    ('COUNTY_Nyeri', 'COUNTY_NYERI.title()'),
    ('COUNTY_Samburu', 'COUNTY_SAMBURU.title()'),
    ('COUNTY_Siaya', 'COUNTY_SIAYA.title()'),
    ('COUNTY_Taita_Taveta', 'COUNTY_TAITA_TAVETA.title()'),
    ('COUNTY_Tana_River', 'COUNTY_TANA_RIVER.title()'),
    ('COUNTY_Tharaka_Nithi', 'COUNTY_THARAKA_NITHI.title()'),
    ('COUNTY_Trans_Nzoia', 'COUNTY_TRANS_NZOIA.title()'),
    ('COUNTY_Uasin_Gishu', 'COUNTY_UASIN_GISHU.title()'),
    ('COUNTY_Vihiga', 'COUNTY_VIHIGA.title()'),
    ('COUNTY_Wajir', 'COUNTY_WAJIR.title()'),
    ('COUNTY_West_Pokot', 'COUNTY_WEST_POKOT.title()'),
)


ROLE_USER = 'USER'
ROLE_VENDOR = 'VENDOR'

ROLE_STAFF = 'STAFF'

ROLE_USER = 'USER'

ROLE_CHOICES =(
(ROLE_VENDOR, ROLE_VENDOR.title()),
(ROLE_STAFF, ROLE_STAFF.title()),
(ROLE_USER, ROLE_USER.title()),
)

IDENTITY_NATIONAL_ID = 'NATIONAL ID'

IDENTITY_PASSPORT = 'PASSPORT'

IDENTITY_DRIVER_LICENCE = 'DRIVER LICENCE'

IDENTITY_CHOICES = (
    (IDENTITY_NATIONAL_ID, IDENTITY_NATIONAL_ID.title()),
    (IDENTITY_PASSPORT, IDENTITY_PASSPORT.title()),
    (IDENTITY_DRIVER_LICENCE, IDENTITY_DRIVER_LICENCE.title()),
)
PAYMENT_METHOD_MOBILE_MONEY = 'MOBILE MONEY'

PAYMENT_METHOD_CARD = 'CARD'

PAYMENT_METHOD_CHOICES = (
    (PAYMENT_METHOD_MOBILE_MONEY, PAYMENT_METHOD_MOBILE_MONEY.title()),
    (PAYMENT_METHOD_CARD, PAYMENT_METHOD_CARD.title()),
)

LIMITED_BUSINESS_ACCOUNT = 'LIMITED_BUSINESS_ACCOUNT'
INDIVIDUAL_BUSINESS_ACCOUNT = 'INDIVIDUAL_BUSINESS_ACCOUNT'
BUSINESS_NAME_ACCOUNT = 'BUSINESS_NAME_ACCOUNT'

BUSINESS_TYPE_CHOICES = (
    (LIMITED_BUSINESS_ACCOUNT, LIMITED_BUSINESS_ACCOUNT.title()),
    (INDIVIDUAL_BUSINESS_ACCOUNT, INDIVIDUAL_BUSINESS_ACCOUNT.title()),
    (BUSINESS_NAME_ACCOUNT, BUSINESS_NAME_ACCOUNT.title()),
)

OPTIONAL_FIELDS = (

)