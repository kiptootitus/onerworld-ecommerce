import axios from "../../utils/AxiosInterceptor";
import { toast } from "react-toastify";

class UserDataService {
    // Helper to extract meaningful error messages
    handleError(error: any, defaultMessage: string) {
        // Extract error message from the response
        const message =
            error?.response?.data?.message ||
            error?.response?.data?.detail ||
            defaultMessage;

        // Show the error to the user using toast
        toast.error(message);

        // Re-throw the error for further handling in thunks or higher up
        throw new Error(message);
    }


async createUser(data: any) {
        return axios.post(`/accounts/vendor/register/`, data);
}




    async getCode(data: any){
      return axios.post(`/accounts/vendor/send-verify-email/`, data);
    }


    async getVerified(data: any){
      return axios.post(`/accounts/vendor/verify-email/`, data);
    }



   async vendorLogin(data: any) {

             return axios.post(`/accounts/token/`, data);

    }
    async getVendor() {

             return  axios.get(`/vendor/`);

    }

    async verifyBusiness(data: any) {
        try {
            const response = await axios.post(`/vendor/verify/business/address/`, data);
            return response.data;
        } catch (error) {
            this.handleError(error, "Error while verifying business.");
        }
    }
}

export default new UserDataService();