from vendor.models import Vendor, VendorManager

class VendorHandler:
    def __init__(self):
        self.vendor_manager = VendorManager()

    def create_update_vendor_by_user(self,data: dict)-> Vendor:
        """
        This method creates or updates vendor object
        :param data{
            'user': The user object
        }
        return:
        """
        return self.create_update_vendor_by_user(data)

    def get_all_vendors(self)-> Vendor.objects:
        """
        This method returns all vendors
        :return: vendor.objects
        """
        return self.get_all_vendors()