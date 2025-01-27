import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import Cookies from "js-cookie";

// const API_URL = "http://api.justshoppinn.com";
const API_URL = import.meta.env.VITE_API_URL;

const instance = axios.create({
	baseURL: API_URL,
	withCredentials: true, // Set globally for all requests
});

instance.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
instance.defaults.headers.common["Access-Control-Allow-Methods"] =
	"GET,PUT,POST,DELETE,PATCH,OPTIONS";
instance.defaults.headers.common["Access-Control-Allow-Headers"] =
	"Origin, X-Requested-With, Content-Type, Accept, Authorization";

instance.defaults.headers.common["Content-Type"] = "application/json";
instance.defaults.headers.common["Accept"] = "application/json";

// Create an Axios interceptor to handle all requests
instance.interceptors.request.use(
	(config: InternalAxiosRequestConfig) => {
		const token = Cookies.get("token");

		if (token && config.headers) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		return config;
	},
	(error: AxiosError) => {
		return Promise.reject(error);
	}
);

// Create an Axios interceptor to handle all responses
instance.interceptors.response.use(
	(response) => {
		return response;
	},
	(error: AxiosError) => {
		if (error.response?.status === 401) {
			// Redirect to the login page if a 401 error occurs
			Cookies.remove("token");
			window.location.reload();
		}
		return Promise.reject(error);
	}
);

export default instance;