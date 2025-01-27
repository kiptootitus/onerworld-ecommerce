import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { createUser, getCode } from "../Redux/Slice/vendorSlice";
import { useAppDispatch, useAppSelector } from "../Redux/store";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import BtnLoader from "../common/BtnLoader";

function SignUp() {
    const dispatch = useAppDispatch();
    const navigate = useNavigate();
    const { user, loading, error } = useAppSelector((state: any) => state.vendor);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

// Display errors from the Redux store
useEffect(() => {
    if (error && typeof error === 'object') {
        Object.entries(error).forEach(([key, value]) => {
            // Ensure each error entry is treated as an array for consistent handling
            const errorMessages = Array.isArray(value) ? value : [value];
            errorMessages.forEach((err) => {
                // Display each error using toast
                toast.error(`${key}: ${err}`, { toastId: `${key}-${err}` });
            });
        });
    } else if (error) {
        // If error is not an object, log it for debugging
        console.error("Unexpected error format:", error);
        toast.error(`Error: ${error}`);
    }
}, [error]);


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        // Validate email format
        if (!/\S+@\S+\.\S+/.test(email)) {
            toast.error("Invalid email format");
            return;
        }

        // Validate password length
        if (password.length < 6) {
            toast.error("Password must be at least 6 characters");
            return;
        }

        // Ensure passwords match
        if (password !== confirmPassword) {
            toast.error("Passwords do not match");
            return;
        }

        // Dispatch createUser if all fields are valid
        try {
             await dispatch(createUser({ email, password })).unwrap();
            toast.success("Account created successfully! Verification code sent to " );
        } catch (err) {
            toast.error("Failed to create user");
        }
    };

    // Send verification code when user email is set in the Redux store
    useEffect(() => {
        if (user?.email) {
            dispatch(getCode({ email: user.email }))
                .unwrap()
                .then(() => {
                    toast.success("Verification code sent successfully!");
                })
                .catch(() => {
                    toast.error("Failed to send verification code");
                });
        }
    }, [user?.email, dispatch]);

    // Redirect to verification page when user exists
    useEffect(() => {
        if (user) {
            navigate("/verify");
        }
    }, [user, navigate]);

    return (
        <div className="bg-gray-100 h-screen w-full flex items-center justify-center">
            <div>
                <h1 className="text-center font-bold text-4xl mb-4">
                    Sell with OnewWorld
                </h1>
                <p className="mb-1 text-lg text-center">
                    Hi there! Welcome to OnewWorld® Seller.
                </p>
                <p className="mb-4 text-lg text-center">
                    Where buyers all over Kenya buy your products.
                </p>
                <div className="bg-white drop-shadow-md rounded-lg px-12 py-8">
                    <h3 className="text-4xl mb-9">Sign-up</h3>
                    <form onSubmit={handleSubmit}>
                        <div className="py-1">
                            <label className="px-1 text-sm text-gray-600">Business Email</label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="text-md outline-none block px-3 py-2 border-2 border-gray rounded-lg w-full bg-white"
                                required
                                pattern="\S+@\S+\.\S+"
                            />
                        </div>
                        <div className="py-1">
                            <label className="px-1 text-sm text-gray-600">Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="text-md outline-none block px-3 py-2 border-2 border-gray rounded-lg w-full bg-white"
                                required
                                minLength={6}
                            />
                        </div>
                        <div className="py-1">
                            <label className="px-1 text-sm text-gray-600">Confirm Password</label>
                            <input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                className="text-md outline-none block px-3 py-2 border-2 border-gray rounded-lg w-full bg-white"
                                required
                                minLength={6}
                            />
                        </div>
                        <button
                            type="submit"
                            className="mt-3 text-lg w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                            disabled={loading}
                        >
                            {loading ? <BtnLoader /> : "Next"}
                        </button>
                    </form>
                    <div className="text-center mt-4">
                        <p className="inline mr-2">Already a seller?</p>
                        <Link to="/signin" className="text-blue-600">
                            Sign In
                        </Link>
                    </div>
                </div>
                <h3 className="text-center text-gray-500 mt-4">
                    {new Date().getFullYear()}, OneWorld.com
                </h3>
            </div>
        </div>
    );
}

export default SignUp;