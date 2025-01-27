import VSignUp from "../screens/signup";
import VSignIn from "../screens/signin";
import { Route, Routes } from "react-router-dom";

import { CiWarning } from 'react-icons/ci';


function index() {
  const isDesktop = window.matchMedia(
    "only screen and (min-width: 761px)"
  ).matches;

  if (isDesktop) {
    return (
      <Routes>
        <Route path="/signup" element={<VSignUp />} />
        <Route path="/signin" element={<VSignIn />} />


      </Routes>
    );
  } else {
    return (
      <div className="">
        <div className="flex items-center justify-center h-screen bg-gray-200">
          <div className="flex flex-col items-center justify-center max-w-2xl">
            <div>
              <CiWarning className="w-20 h-20 text-yellow-400" />
            </div>
            <h1 className="mb-3 text-3xl font-bold text-center text-black-100">
              Sorry, This website is only available on desktop devices.
            </h1>
            <p className="text-center text-black-100 text-lg">
              We’ll notify you when mobile version in available
            </p>
          </div>
        </div>
      </div>
    );
  }
}

export default index;