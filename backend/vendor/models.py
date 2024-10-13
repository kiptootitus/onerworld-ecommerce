import datetime
import logging

from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Address
from billing.models import Billing
from config_master import IDENTITY_CHOICES, OPTIONAL_FIELDS, IDENTITY_NATIONAL_ID, PAYMENT_METHOD_CARD, PAYMENT_METHOD_CHOICES, BUSINESS_TYPE_CHOICES , LIMITED_BUSINESS_ACCOUNT, INDIVIDUAL_BUSINESS_ACCOUNT, BUSINESS_NAME_ACCOUNT
from oneworld.models import BaseModel
from orders.models import OrderDetails
from plans.models import VendorSellingPlans

log = logging.getLogger(__name__)


class VendorAccountModel(BaseModel):
    """
    This model contains fields that are available in all the models
    """
    business_name = models.CharField(default='', max_length=500, null=False, blank=False)
    display_name = models.CharField(default='', max_length=500, null=False, blank=False, unique=True)
    seller_name = models.CharField(default='', max_length=500, null=False, blank=False)
    company_registration_number = models.CharField(default='', max_length=500, null=False, blank=False)
    t_pin = models.CharField(default='', max_length=500, null=False, blank=False)
    t_pin_file = models.FileField(null=True, blank=True, upload_to='vendor/business_documents/')
    first_name = models.CharField(default='', max_length=500, null=False, blank=False)
    middle_name = models.CharField(default='', max_length=500, null=False, blank=False)
    last_name = models.CharField(default='', max_length=500, null=False, blank=False)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(null=True, blank=True)
    payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICES, default=PAYMENT_METHOD_CARD, max_length=100,
                                      null=True, blank=True)
    additional_files = models.FileField(null=True, blank=True, upload_to='vendor/business_documents/')

    class Meta:
        abstract = True


class LimitedBusinessAccount:
    pass


class IndividualAccount:
    pass


class BusinessNameAccount:
    pass


class Vendor(BaseModel):
    """
    This hold information about the seller
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False, related_name='vendors')
    country_of_citizenship = models.CharField(default='', max_length=500, null=True, blank=True)
    country_of_birth = models.CharField(default='', max_length=500, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    proof_of_identity = models.CharField(choices=IDENTITY_CHOICES, default=IDENTITY_NATIONAL_ID, max_length=100,
                                         null=True, blank=True)
    identity_number = models.CharField(null=True, blank=True, default='', max_length=500, )
    identity_upload = models.FileField(upload_to='vendor/documents/', blank=True, null=True)
    date_of_expiry = models.DateField(null=True, blank=True)
    country_of_issue = models.CharField(default='', max_length=500, null=True, blank=True)
    residential_address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True,
                                            related_name='vendor_resident_addresses')
    phone_number = PhoneNumberField(blank=True)
    selling_plan = models.ForeignKey(VendorSellingPlans, on_delete=models.PROTECT, null=True, blank=True,
                                     related_name='vendors')
    business_type_name = models.CharField(choices=BUSINESS_TYPE_CHOICES, default='', max_length=100,
                                          null=True, blank=True)
    is_active = models.BooleanField(default=False)
    additional_details = models.CharField(
        default='', max_length=1000,
        null=True,
        blank=True,
        help_text="Any text can be added here. For instance you can use it to save the progress of the "
                  "vendor registration so as to know where to redirect when they login."
    )

    def save(self, *args, **kwargs):
        """
        This method overrides the default save method and check to see if the business type name has changed. If so a
        business type with the name will be created for the vendor. For instance if the value of the business type name
        is limited_business_account, LimitedBusinessAccount object will be created for a vendor.
        :param args:
        :param kwargs:
        :return:
        """
        try:
            if self.pk is not None and self.business_type_name:
                initial = Vendor.objects.get(id=self.pk)
                initial_json, final_json = initial.__dict__.copy(), self.__dict__.copy()
                if initial_json.get('business_type_name') != final_json.get('business_type_name'):
                    return  initial_json.get('business_type_name') != final_json.get('business_type_name')
            return self.pk is None and self.business_type_name
        except Exception as e:
            log.error('Error: An error occurred while creating vendor business type %s' % str(e))
        super(Vendor, self).save(*args, **kwargs)

    def __str__(self):
        return f'Vendor - {str(self.user.username)} - ({str(self.business_type_name)})'

    def is_fully_filled(self):
        """ Checks if all the fields have been filled """
        fields_names = [f.name for f in self._meta.get_fields()]
        remaining_fields = []
        for field_name in fields_names:
            if field_name in OPTIONAL_FIELDS:
                continue
            try:
                value = getattr(self, field_name)
                if value is None or value == '':
                    remaining_fields.append(field_name)
            except Exception as e:
                continue
        return remaining_fields

    def get_limited_business_account(self) -> LimitedBusinessAccount or None:
        """
        This method returns limited business account of a vendor
        :return: LimitedBusinessAccount or None
        """
        if LimitedBusinessAccount.objects.filter(vendor=self):
            return LimitedBusinessAccount.objects.filter(vendor=self).last()

    def get_business_name_account(self) -> BusinessNameAccount or None:
        """
        This method returns business name account of a vendor
        :return: BusinessNameAccount or None
        """
        if BusinessNameAccount.objects.filter(vendor=self):
            return BusinessNameAccount.objects.filter(vendor=self).last()

    def get_individual_account(self) -> IndividualAccount or None:
        """
        This method returns individual account of a vendor
        :return: IndividualAccount or None
        """
        if IndividualAccount.objects.filter(vendor=self):
            return IndividualAccount.objects.filter(vendor=self).last()

    def active_business_type_account(self):
        """
        This method returns the active business account type for a particular vendor
        :return:
        """
        if self.get_limited_business_account() and self.business_type_name == LIMITED_BUSINESS_ACCOUNT:
            return self.get_limited_business_account()

        if self.get_individual_account() and self.business_type_name == INDIVIDUAL_BUSINESS_ACCOUNT:
            return self.get_individual_account()

        if self.get_business_name_account() and self.business_type_name == BUSINESS_NAME_ACCOUNT:
            return self.get_business_name_account()

    def get_registration_status(self):
        """
        This method returns the registration status of a vendor
        :return: dict
        """
        remaining_items = []
        if not self.user.is_active:
            remaining_items.append('Please verify Email')
        if not self.selling_plan:
            remaining_items.append('Please select business plan')
        has_selected_business_type = False

        remaining_fields = self.is_fully_filled()
        remaining_items += remaining_fields
        if self.active_business_type_account():
            business_type_account = self.active_business_type_account()
            if business_type_account.address and not business_type_account.address.is_verified:
                remaining_items.append('Business Address has not been verified')
        return remaining_items


class VendorManager:

    def create_update_vendor_by_user(self, data: dict) -> Vendor:
        """
        This method creates or updates a vendor object
        :param data: {
            'user': The user object,
        }
        :return:
        """
        if Vendor.objects.filter(user=data.get('user')).exists():
            return Vendor.objects.filter(user=data.get('user')).last()
        return Vendor.objects.create(
            user=data.get('user'),
        )

    def get_all_vendors(self) -> Vendor.objects:
        """
        This method returns all the vendors
        :return: Vendor Objects
        """
        return Vendor.objects.all().select_related('user')



    def update_seller_information(self, data: dict) -> Vendor:
        """
        This method upadates the seller information of a vendor
        :param data: {
            'vendor_id': The ID value of the vendor,
            'image': '',
            'country_of_citizenship': '',
            'country_of_birth': '',
            'date_of_birth': '',
            'proof_of_identity': '',
            'identity_number': '',
            'date_of_expiry': '',
            'country_of_issue': '',
            'phone_number': '',
            'created_by': '',
        }
        :return:
        """
        vendor = Vendor.objects.get(id=data.get('vendor_id'))
        vendor.country_of_citizenship = data.get('country_of_citizenship')
        vendor.country_of_birth = data.get('country_of_birth')
        vendor.date_of_birth = datetime.datetime.strptime(data.get('date_of_birth'), '%d-%m-%Y')
        vendor.proof_of_identity = data.get('proof_of_identity')
        vendor.identity_number = data.get('identity_number')
        vendor.identity_upload = data.get('identity_upload')
        vendor.date_of_expiry = datetime.datetime.strptime(data.get('date_of_expiry'), '%d-%m-%Y')
        vendor.country_of_issue = data.get('country_of_issue')
        vendor.phone_number = data.get('phone_number')
        vendor.modified_by = data.get('created_by')
        vendor.save()
        return vendor







