import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import UserDataService from "../Service/vendorService";
import Cookies from 'js-cookie';
import { toast } from "react-toastify";

// Utility function for handling async errors
const handleAsyncError = async (error: any, rejectWithValue: any) => {
    console.error("API Error:", error); // Debugging
    if (error.response) {
        const backendErrors = error.response.data;
        if (typeof backendErrors === "object" && backendErrors !== null) {
            const errorMessages = Object.entries(backendErrors)
                .map(([field, messages]) => {
                    const fieldMessages = Array.isArray(messages)
                        ? messages.join(" ")
                        : messages;
                    return `${field}: ${fieldMessages}`;
                })
                .join(" ");
            return rejectWithValue(errorMessages);
        }
        return rejectWithValue(error.response.data.message || "An unknown error occurred.");
    }
    return rejectWithValue(error?.message || "An unknown error occurred.");
};

// Define Types
interface User {
    id: string;
    email: string;
    name: string;
}

interface VendorMessage {
    email_verified?: boolean;
    [key: string]: any;
}

interface StateProps {
    user: User | null;
    userInfo: any; // Replace with a defined type if structure is known
    message: VendorMessage;
    error: string | null;
    loading: boolean;
}

// Define Redux Thunks
export const createUser = createAsyncThunk("User/createUser", async (data: any, { rejectWithValue }) => {
    try {
        const res = await UserDataService.createUser(data);
        Cookies.set("vendor_email", res.data.email);
        return res.data;
    } catch (error) {
        return handleAsyncError(error, rejectWithValue);
    }
});

export const getCode = createAsyncThunk("User/getCode", async (data: any, { rejectWithValue }) => {
    try {
        const res = await UserDataService.getCode(data);
        return res.data;
    } catch (error) {
        return handleAsyncError(error, rejectWithValue);
    }
});

export const getVerified = createAsyncThunk("User/getVerified", async (data: any, { rejectWithValue }) => {
    try {
        const res = await UserDataService.getVerified(data);
        return res.data;
    } catch (error) {
        return handleAsyncError(error, rejectWithValue);
    }
});

export const vendorLogin = createAsyncThunk("User/vendorLogin", async (data: any, { rejectWithValue }) => {
    try {
        const res = await UserDataService.vendorLogin(data);
        Cookies.set("token", res.data.access);
        return res.data;
    } catch (error) {
        return handleAsyncError(error, rejectWithValue);
    }
});

export const getVendor = createAsyncThunk("Vendor/getVendor", async (_, { getState, rejectWithValue }) => {
    const { userInfo } = (getState() as any).vendor;
    if (userInfo) {
        return userInfo; // Return cached userInfo if available
    }
    try {
        const res = await UserDataService.getVendor();
        return res.data;
    } catch (error) {
        return handleAsyncError(error, rejectWithValue);
    }
});

export const verifyBusiness = createAsyncThunk("User/verifyBusiness", async (data: any, { rejectWithValue }) => {
    try {
        const res = await UserDataService.verifyBusiness(data);
        return res.data;
    } catch (error) {
        return handleAsyncError(error, rejectWithValue);
    }
});

// Initial State
const initialState: StateProps = {
    user: null,
    userInfo: null,
    message: {},
    error: null,
    loading: false,
};

// Vendor Slice
const vendorSlice = createSlice({
    name: "Vendor",
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        const handlePending = (state: StateProps) => {
            state.loading = true;
            state.error = null;
        };

        const handleRejected = (state: StateProps, action: any) => {
            state.loading = false;
            state.error = action.payload;
            if (action.payload) {
                if (typeof action.payload === "string") {
                    if (action.payload.includes("must be unique")) {
                        toast.error("This field must be unique. Username/Email is already in use.");
                    } else if (action.payload.includes("Invalid credentials")) {
                        toast.error("Incorrect username or password. Please try again.");
                    } else {
                        toast.error(action.payload);
                    }
                } else {
                    console.error("Unexpected error format:", action.payload);
                    toast.error("An unexpected error occurred. Please try again.");
                }
            } else {
                toast.error("An unknown error occurred.");
            }
        };

        builder
            .addCase(createUser.pending, handlePending)
            .addCase(createUser.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload;
                toast.success("User created successfully!");
            })
            .addCase(createUser.rejected, handleRejected)

            .addCase(getCode.pending, handlePending)
            .addCase(getCode.fulfilled, (state, action) => {
                state.loading = false;
                state.message = action.payload;
                toast.success("Code sent successfully!");
            })
            .addCase(getCode.rejected, handleRejected)

            .addCase(getVerified.pending, handlePending)
            .addCase(getVerified.fulfilled, (state, action) => {
                state.loading = false;
                state.message = {
                    ...state.message,
                    email_verified: !!action.payload?.email_verified,
                };
                if (action.payload?.email_verified) {
                    Cookies.remove("vendor_email");
                    toast.success("Email verified successfully!");
                }
            })
            .addCase(getVerified.rejected, handleRejected)

            .addCase(vendorLogin.pending, handlePending)
            .addCase(vendorLogin.fulfilled, (state, action) => {
                state.loading = false;
                if (action.payload && action.payload.access) {
                    state.user = action.payload;
                    localStorage.setItem("user", JSON.stringify(action.payload));
                    toast.success("Login successful!");
                } else {
                    console.error("Unexpected login payload:", action.payload);
                    toast.error("An unexpected error occurred. Please try again.");
                }
            })
            .addCase(vendorLogin.rejected, handleRejected)

            .addCase(getVendor.pending, handlePending)
            .addCase(getVendor.fulfilled, (state, action) => {
                state.loading = false;
                state.userInfo = action.payload;
            })
            .addCase(getVendor.rejected, handleRejected);
    },
});

export default vendorSlice.reducer;